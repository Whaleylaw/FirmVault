import { promises as fs } from "fs";
import path from "path";
import matter from "gray-matter";
import simpleGit, { SimpleGit } from "simple-git";

/**
 * Vault access layer. Clones the firmvault repo into CACHE_DIR on
 * first use, then reads markdown from disk. All write-path commits
 * also go through this module so there's a single simple-git handle.
 *
 * This deliberately does NOT expose graph-queries or indexed search.
 * The firmvault contract is "plain text + grep"; we follow it.
 */

export interface CaseFrontmatter {
  schema_version?: number;
  case_id?: string;
  client_name?: string;
  case_type?: string;
  status?: string;
  date_of_incident?: string;
  jurisdiction?: string;
  case_number?: string;
  pilot?: boolean;
  landmarks?: Record<string, boolean>;
  case_summary_written?: boolean;
  // Catch-all for arbitrary frontmatter keys set downstream.
  [key: string]: unknown;
}

export interface CaseFile {
  slug: string;
  filePath: string; // absolute path inside the cache
  frontmatter: CaseFrontmatter;
  body: string;
  sections: Record<string, string>;
  documents: string[]; // filenames under cases/<slug>/documents/
}

export interface ActivityEntry {
  file: string;
  date?: string;
  category?: string;
  excerpt: string;
}

const DEFAULT_CACHE_DIR = path.resolve(process.cwd(), ".cache/firmvault");
const DEFAULT_REPO_URL =
  process.env.FIRMVAULT_REPO_URL ??
  "https://github.com/Whaleylaw/firmvault.git";

function cacheDir(): string {
  return path.resolve(process.env.CACHE_DIR ?? DEFAULT_CACHE_DIR);
}

let ensurePromise: Promise<SimpleGit> | null = null;

/**
 * Ensure the firmvault repo exists in the cache. On first call this
 * clones; on subsequent calls it just returns the simple-git handle.
 */
export async function ensureVault(): Promise<SimpleGit> {
  if (ensurePromise) return ensurePromise;
  ensurePromise = (async () => {
    const dir = cacheDir();
    await fs.mkdir(path.dirname(dir), { recursive: true });
    const exists = await fs
      .stat(path.join(dir, ".git"))
      .then(() => true)
      .catch(() => false);
    if (!exists) {
      const git = simpleGit();
      await git.clone(DEFAULT_REPO_URL, dir, ["--depth", "50"]);
    }
    return simpleGit(dir);
  })();
  return ensurePromise;
}

/** Pull the latest changes from origin. Idempotent. */
export async function refreshVault(): Promise<{ head: string }> {
  const git = await ensureVault();
  await git.fetch("origin");
  // Pull the current branch so reads see new landmark updates.
  await git.pull().catch(() => {
    // If pull fails (dirty working tree, detached HEAD), log and
    // proceed — reads can still hit the existing snapshot.
  });
  const head = await git.revparse(["HEAD"]);
  return { head: head.trim() };
}

export async function vaultRoot(): Promise<string> {
  await ensureVault();
  return cacheDir();
}

/** List every case slug under cases/ in the cache. */
export async function listCaseSlugs(): Promise<string[]> {
  const root = await vaultRoot();
  const casesDir = path.join(root, "cases");
  const entries = await fs.readdir(casesDir, { withFileTypes: true }).catch(() => []);
  return entries
    .filter((e) => e.isDirectory())
    .map((e) => e.name)
    .sort();
}

/** Read a single case file fully. Returns null if the slug is missing. */
export async function readCase(slug: string): Promise<CaseFile | null> {
  const root = await vaultRoot();
  const filePath = path.join(root, "cases", slug, `${slug}.md`);
  const raw = await fs.readFile(filePath, "utf8").catch(() => null);
  if (raw == null) return null;
  const parsed = matter(raw);
  const frontmatter = (parsed.data as CaseFrontmatter) ?? {};
  const sections = splitSections(parsed.content);
  const documents = await listDocuments(slug);
  return {
    slug,
    filePath,
    frontmatter,
    body: parsed.content,
    sections,
    documents,
  };
}

/** Read all cases. Convenience wrapper for the landing page. */
export async function readAllCases(): Promise<CaseFile[]> {
  const slugs = await listCaseSlugs();
  const out: CaseFile[] = [];
  for (const slug of slugs) {
    const c = await readCase(slug);
    if (c) out.push(c);
  }
  return out;
}

async function listDocuments(slug: string): Promise<string[]> {
  const root = await vaultRoot();
  const docsDir = path.join(root, "cases", slug, "documents");
  const entries = await fs.readdir(docsDir, { withFileTypes: true }).catch(() => []);
  return entries.filter((e) => e.isFile()).map((e) => e.name).sort();
}

/** Read the 10 most recent activity log entries for a case. */
export async function readRecentActivity(
  slug: string,
  limit = 10,
): Promise<ActivityEntry[]> {
  const root = await vaultRoot();
  const logDir = path.join(root, "cases", slug, "Activity Log");
  const entries = await fs.readdir(logDir, { withFileTypes: true }).catch(() => []);
  const files = entries.filter((e) => e.isFile()).map((e) => e.name).sort().reverse();
  const out: ActivityEntry[] = [];
  for (const file of files.slice(0, limit)) {
    const full = await fs.readFile(path.join(logDir, file), "utf8").catch(() => null);
    if (!full) continue;
    const parsed = matter(full);
    out.push({
      file,
      date: (parsed.data as Record<string, string>).date,
      category: (parsed.data as Record<string, string>).category,
      excerpt: parsed.content.split("\n").slice(0, 4).join("\n"),
    });
  }
  return out;
}

/**
 * Split the markdown body into { heading: content } chunks. Very
 * deliberately naive — the contract says agents grep for headings,
 * so we do the same.
 */
function splitSections(body: string): Record<string, string> {
  const lines = body.split("\n");
  const out: Record<string, string> = {};
  let current: string | null = null;
  let buf: string[] = [];
  for (const line of lines) {
    const m = line.match(/^##\s+(.*)$/);
    if (m) {
      if (current) out[current] = buf.join("\n").trim();
      current = m[1].trim();
      buf = [];
    } else if (current) {
      buf.push(line);
    }
  }
  if (current) out[current] = buf.join("\n").trim();
  return out;
}

/**
 * Write a file into the vault cache and commit. Used by the worker.
 * caller is responsible for passing an absolute-to-repo-relative path
 * (e.g. "cases/jordan-brown/documents/summary.md").
 */
export async function writeVaultFile(
  relPath: string,
  contents: string,
  commitMessage: string,
): Promise<{ sha: string }> {
  const git = await ensureVault();
  const root = await vaultRoot();
  const abs = path.join(root, relPath);
  await fs.mkdir(path.dirname(abs), { recursive: true });
  await fs.writeFile(abs, contents, "utf8");
  await git.add(relPath);
  // Commit may fail if nothing changed — swallow that specific case.
  try {
    await git.commit(commitMessage, undefined, {
      "--author": "Cockpit Worker <cockpit@firmvault.local>",
    });
  } catch (err) {
    // No-op: likely nothing-to-commit.
  }
  const sha = await git.revparse(["HEAD"]);
  return { sha: sha.trim() };
}

/**
 * Set a single key in the frontmatter of a case file and commit.
 * Preserves every other key and the body.
 */
export async function setFrontmatterKey(
  slug: string,
  key: string,
  value: unknown,
  commitMessage: string,
): Promise<void> {
  const root = await vaultRoot();
  const rel = path.join("cases", slug, `${slug}.md`);
  const abs = path.join(root, rel);
  const raw = await fs.readFile(abs, "utf8");
  const parsed = matter(raw);
  const data = { ...parsed.data, [key]: value };
  const rebuilt = matter.stringify(parsed.content, data);
  await writeVaultFile(rel, rebuilt, commitMessage);
}

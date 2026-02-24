"""
Slug Generator for Case Directory Names

Converts client names into ASCII-only, lowercase slugs suitable for
directory names in the vault structure. Handles collision detection
with numeric suffixes.

Rules (from CONTEXT.md locked decisions):
- Full client name slug: "Muhammad Alif" -> "muhammad-alif"
- ASCII-only: strip apostrophes, accents (O'Brien -> obrien, K'daya -> kdaya)
- Lowercase with hyphens as separator
- Numeric suffix for collisions: first gets no suffix, second gets "-2"
- The function MUTATES the existing_slugs set (adds the new slug)

Usage:
    from scripts.migrate.slug_generator import generate_case_slug

    existing = set()
    slug1 = generate_case_slug("Muhammad Alif", existing)  # "muhammad-alif"
    slug2 = generate_case_slug("John Smith", existing)     # "john-smith"
    slug3 = generate_case_slug("John Smith", existing)     # "john-smith-2"
"""

from slugify import slugify


def generate_case_slug(client_name: str, existing_slugs: set[str]) -> str:
    """Generate a unique case slug from a client name.

    Produces an ASCII-only, lowercase, hyphen-separated slug from the
    given client name. If the slug already exists in existing_slugs,
    appends a numeric suffix (-2, -3, etc.) for uniqueness.

    The function MUTATES existing_slugs by adding the newly generated slug.

    Parameters
    ----------
    client_name : str
        The client's full name (e.g., "Muhammad Alif", "K'daya Austin").
    existing_slugs : set[str]
        Set of slugs already in use. Will be mutated to include the new slug.

    Returns
    -------
    str
        A unique ASCII slug (e.g., "muhammad-alif", "john-smith-2").

    Raises
    ------
    ValueError
        If client_name is empty or produces an empty slug.
    """
    if not client_name or not client_name.strip():
        raise ValueError("client_name must be a non-empty string")

    # Strip apostrophes and curly quotes BEFORE slugification so they don't
    # become hyphens. Per CONTEXT.md: O'Brien -> obrien, K'daya -> kdaya.
    cleaned = client_name.replace("'", "").replace("\u2019", "").replace("\u2018", "")

    base = slugify(cleaned, separator="-", lowercase=True)

    if not base:
        raise ValueError(
            f"client_name '{client_name}' produced an empty slug after slugification"
        )

    if base not in existing_slugs:
        existing_slugs.add(base)
        return base

    counter = 2
    while f"{base}-{counter}" in existing_slugs:
        counter += 1

    slug = f"{base}-{counter}"
    existing_slugs.add(slug)
    return slug

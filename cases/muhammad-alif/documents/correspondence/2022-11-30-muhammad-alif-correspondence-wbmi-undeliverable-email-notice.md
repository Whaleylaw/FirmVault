---
case_slug: muhammad-alif
created_at: 2026-02-17 00:09:45.209000+00:00
document_category: correspondence
document_type: correspondence
extraction_method: native_text
legacy_case_id: 2022-11-08-MVA-001
mime_type: message/rfc822
page_count: 1
quality_score: 90
source_file: /Users/aaronwhaley/Whaley Law Firm Dropbox/Litigation/Active/Muhammad-Alif-MVA-11-08-2022/Correspondence/Email/2022-11-30-Muhammad-Alif-Correspondence-WBMI-Undeliverable-Email-Notice.eml
source_hash: sha256:d25a6309e94d454e1a8194a56ce0a5b034be1c336166ea46d08f68a123da7d3d
---

Subject: Undeliverable: Re: [External]Claim: AP92071 - Muhammad Alif
From: [EMAIL-1]
To: sarena@whaleylawfirm.com
Date: 2022-11-30T08:45:53-06:00
Delivery has failed to these recipients or groups:

[EMAIL-16]<mailto:[EMAIL-15]>
The email address you entered couldn't be found. Please check the recipient's email address and try to resend the message. If the problem continues, please contact your email admin.








Diagnostic information for administrators:

Generating server: wiwpexc01.wbmi.com

[EMAIL-14]
Remote Server returned '550 5.1.10 RESOLVER.ADR.RecipientNotFound; Recipient not found by SMTP address lookup'

Original message headers:

Received: from wiwpexc01.wbmi.com (10.185.8.28) by wiwpexc01.wbmi.com
 (10.185.8.28) with Microsoft SMTP Server (version=TLS1_2,
 cipher=TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256) id 15.1.2507.16; Wed, 30 Nov
 2022 08:45:53 -0600
Received: from NAM12-DM6-obe.outbound.protection.outlook.com (10.2.1.6) by
 wiwpexc01.wbmi.com (10.185.8.28) with Microsoft SMTP Server (version=TLS1_2,
 cipher=TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256) id 15.1.2507.16 via Frontend
 Transport; Wed, 30 Nov 2022 08:45:53 -0600
ARC-Seal: i=1; a=rsa-sha256; s=arcselector9901; d=microsoft.com; cv=none;
 b=SQ0qy8v5yd8wu/AkgxP00DcsYOnJH3BZVkVGsFqleKLaeza7B3n2wGKJ5CDLscpjG4evRCKUgViUIvvwqsd/kYPO0D96k0IqJ+58KHT9eOj38rM+fdkMHmrZwGr6pvdjoEQUHKkzZ39NDZm8kOhm5uNf+AufMHeWcuaKRst0cnAMs0XH3UaIuDer/+Z9SFMtcUEoKK9D6VYSUK2zIWkmrp/j+KmbpHg1ufCb3vM5ZwdxI/ipQg4LCK34G4yZt3Lu4CIFxPS9VUqtDjWpRhjyYD/r8r8XpsdDmpRkq0WUpasvSkP96Dh7Bs++e8pfqvCMPxrBjaGe6bMi2VmKR2Wqqg==
ARC-Message-Signature: i=1; a=rsa-sha256; c=relaxed/relaxed; d=microsoft.com;
 s=arcselector9901;
 h=From:Date:Subject:Message-ID:Content-Type:MIME-Version:X-MS-Exchange-AntiSpam-MessageData-ChunkCount:X-MS-Exchange-AntiSpam-MessageData-0:X-MS-Exchange-AntiSpam-MessageData-1;
 bh=dsTgWDoXo7s9e/X8K4hQNBd5IxoUA2/Tg38sjoA+UVQ=;
 b=RYB3Z0y1/r3ur+RwEMwRTlEzZN4Zk/3kCBTKva+lytKin97iRKEQx1wNS0X8XgjfdudKYUeykJLedMc85CatyYMpUzXVJPPwOfkYGN3EJG0NbgLrvFu8HH43Auqb3UlBqR5cir4lDf0+GX5e36dpwMS9ThKM/AZM2HddVRXBP+WCdV+6EuxpKeb6gU4ZvU1EqLxm61hpV1d6jeeSU7dgxxnOZhIH9YRs3iVWGnRuJEOZ91EP7kp78ZDyLoLv/rR5Cn+5fUWUCvSVvDJvB7epXA5k3bppVbIWGKVeY9Tn+pPa7puFOJN/CULGeA+y0hV30G4IrQyYrDpVUY6/KdrtiQ==
ARC-Authentication-Results: i=1; mx.microsoft.com 1; spf=none (sender ip is
 209.85.214.171) smtp.rcpttodomain=wbmi.com smtp.mailfrom=whaleylawfirm.com;
 dmarc=none action=none header.from=whaleylawfirm.com; dkim=pass (signature
 was verified) header.d=whaleylawfirm-com.20210112.gappssmtp.com; arc=none (0)
Received: from SA1PR03CA0007.namprd03.prod.outlook.com (2603:10b6:806:2d3::16)
 by PH0PR17MB4718.namprd17.prod.outlook.com (2603:10b6:510:86::16) with
 Microsoft SMTP Server (version=TLS1_2,
 cipher=TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384) id 15.20.5857.18; Wed, 30 Nov
 2022 14:45:50 +0000
Received: from SN1NAM02FT0064.eop-nam02.prod.protection.outlook.com
 (2603:10b6:806:2d3:cafe::7d) by SA1PR03CA0007.outlook.office365.com
 (2603:10b6:806:2d3::16) with Microsoft SMTP Server (version=TLS1_2,
 cipher=TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384) id 15.20.5857.23 via Frontend
 Transport; Wed, 30 Nov 2022 14:45:50 +0000
Authentication-Results: spf=none (sender IP is 209.85.214.171)
 smtp.mailfrom=whaleylawfirm.com; dkim=pass (signature was verified)
 header.d=whaleylawfirm-com.20210112.gappssmtp.com;dmarc=none action=none
 header.from=whaleylawfirm.com;compauth=pass reason=106
Received-SPF: None (protection.outlook.com: whaleylawfirm.com does not
 designate permitted sender hosts)
Received: from mail-pl1-f171.google.com (209.85.214.171) by
 SN1NAM02FT0064.mail.protection.outlook.com (10.97.4.66) with Microsoft SMTP
 Server (version=TLS1_2, cipher=TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384) id
 15.20.5880.8 via Frontend Transport; Wed, 30 Nov 2022 14:45:49 +0000
Received: by mail-pl1-f171.google.com with SMTP id k7so16875602pll.6
        for <[EMAIL-13]>; Wed, 30 Nov 2022 06:45:49 -0800 (PST)
DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed;
        d=whaleylawfirm-com.20210112.gappssmtp.com; s=20210112;
        h=to:subject:message-id:date:from:in-reply-to:references:mime-version
         :from:to:cc:subject:date:message-id:reply-to;
        bh=dsTgWDoXo7s9e/X8K4hQNBd5IxoUA2/Tg38sjoA+UVQ=;
        b=KyBVGYgikon62FeyhlvJVTpNezjlBIU/U9LuGEJFIut6P2Vzq+eT8gTKE+0E63TzPO
         47QgisgTHdrsLgEZDW2T2y9y2EozdyQWfgLk2/xyBVxikSc5RfIdFoONxA66iP6Zknmg
         kntJ7Cf1G1aTaeK04rL0IiiNJ2MAPNzaMrmwhxaIBaVzC0BArB5I6CHGC99hqr98ZK/P
         qHf2M+YJQGmzKWXDkHEkjD/g1tFJaJnojUURrXGj8b5oFbkyxyJeD4rM0xPNWmc/a/EF
         mJuOL2YMulj1CVeh+U3bnPxQiiGNrJ59mQAOCyziZowG2RD77BD88IkUidr/0X0LkkXV
         7zqA==
X-Google-DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed;
        d=1e100.net; s=20210112;
        h=to:subject:message-id:date:from:in-reply-to:references:mime-version
         :x-gm-message-state:from:to:cc:subject:date:message-id:reply-to;
        bh=dsTgWDoXo7s9e/X8K4hQNBd5IxoUA2/Tg38sjoA+UVQ=;
        b=3oB/Bo/nfCqxIHOvSm0Ttx97qNLQoqd15DJssks/MsRmC2KN4CG+55X0fhAIdCoDNr
         yBoy5qZcozCcVdwTkcfaoXna+foQuN+3TEp0bGSGcFTMirUkFSB951C2jVIdLqn2+FZ2
         rhkd1XiYL/4YJFoWeoQNY70aypoqndm4ll5EfwBw8c1RcY9sPJekOk5ZbKV8zJ6j5pyr
         Bfcwr+AmsNJrTcjvRDNCYbZuN8bzG9FjHHWAR0AznOLYIy9Mfj05PkB4i3SZIW5a9vlY
         FwvX7cX6AJ/g1WlH1PoYLQkXsIgBRRwbbfz1iPSsYFLKi96aKwJ+RO3qTgQ4Sc11F4wI
         v3Fg==
X-Gm-Message-State: ANoB5pnydlBepGIE4/Z1ue5QzPXdwKB7VRZrwnEp/Or+dwqMiaZVQ57x
        90gRgkX2FfZLr0n5KTlK52pAhujqKBEw8li/SvKHPBun6gw=
X-Google-Smtp-Source: AA0mqf6qGfVxHk9bqe/MQAAU7G8XiCvmN1dXMMcFGGh7ACYWVrtmdPfz3+wr/EV7/LKuCgRwkyHV5hEArj4EetQjbP8=
X-Received: by 2002:a17:903:481:b0:189:809e:3956 with SMTP id
 jj1-20020a170903048100b00189809e3956mr18672426plb.121.1669819549002; Wed, 30
 Nov 2022 06:45:49 -0800 (PST)
MIME-Version: 1.0
References: <[EMAIL-12]>
 <[EMAIL-11]>
 <[EMAIL-10]>
 <CAAqCzed=[EMAIL-9]>
 <[EMAIL-10]>
 <CAAqCzef3hmsrjomzL7PL+QgYgqZ=Z0=[EMAIL-11]> <[EMAIL-12]>
In-Reply-To: <[EMAIL-13]>
From: Sarena Tuttle <sarena@whaleylawfirm.com>
Date: Wed, 30 Nov 2022 09:45:59 -0500
Message-ID: <CAAqCzefDB=meuWZJ-A7-LGqw-oG+Z9YnGJ_Ma0eYkS6Yt=[EMAIL-14]>
Subject: Re: [External]Claim: AP92071 - Muhammad Alif
To: "Becerra, Ashley" <[EMAIL-15]>, <[EMAIL-16]>
Content-Type: multipart/alternative; boundary="0000000000000ec75905eeb12970"
Return-Path: sarena@whaleylawfirm.com
X-EOPAttributedMessage: 0
X-EOPTenantAttributedMessage: 48b0431c-82f6-4ad2-a023-ac96dbf5614e:0
X-MS-PublicTrafficType: Email
X-MS-TrafficTypeDiagnostic: SN1NAM02FT0064:EE_|PH0PR17MB4718:EE_
X-MS-Office365-Filtering-Correlation-Id: 2a730d71-15c9-4698-b107-08dad2e192c4
X-MS-Exchange-AtpMessageProperties: SA|SL
X-Microsoft-Antispam: BCL:0;
X-Microsoft-Antispam-Message-Info: =?utf-8?B?eEJvQlhsNjNENVByc1RndHdGM0NTZUlFSUpUSjdKVFY3ZjRGRnFUaDEyQXBL?=
 =?utf-8?B?N0hxU1Zpb1lVbEVRd0QrOHBKMnl4aVQybUpNQW1yQkJrQ0hSNnVhVUY3VkVw?=
 =?utf-8?B?dXZJalFkckZxN2R4eGg2ZTFlWWVBRVl5K3l2amtGbGJDV0dYVW9QWWlhWWc2?=
 =?utf-8?B?UzBGaE5FZ1RyazdMR0phbER3ancxWlEzUnN2cm5JUDJ4Y0ZMWHc0SEFJWmd5?=
 =?utf-8?B?TUVyMzNJRHJZRjVTRm1VMjV0bVlkTnNOZEZjVGw4Lzluekw5S0tucVZoQ3or?=
 =?utf-8?B?QjFQU29JOXZvekFwUFJqUXBmbHVtYnZtVTgwTkVPWU5SeUk2SVRHR1R6NjZK?=
 =?utf-8?B?eEJkdS9hYjlGOWZRanNqQlgvSWFTdUh3WjkvNmlvSU5XbURFcnFxUVRSOTFX?=
 =?utf-8?B?TllGQm5JUGpNaXJva0IyZi9ISzlmV0xtVkNiQXdJR20yMGtSYm9ZWk1pbW5P?=
 =?utf-8?B?K0tFRDN4U3M3TEo5UWNnSStSS2g4WGR6NjBYZzJaVmJIdVIza1dqUUJVNE1F?=
 =?utf-8?B?M3FCbldDa0xJNVJlQ29XNWhUdTRXUk9vM1NlN2pCWXdOS3VaTVdEckxuQjFw?=
 =?utf-8?B?Yndqd1FJaWlEaTBrZEhYZjBiSnJOZDJ3eWh1a3pjc251SlRsNTFtaWdVQ3pB?=
 =?utf-8?B?UUJ3RXlBc2VrbnFzN3Q3ck1XNW1uSzgyNjFZZVplYitkMTk1MjNCVnV1dnNG?=
 =?utf-8?B?aE5IRUtSbXkxYXlLaXVnWWZHbHlwUDZvclgvUzdRQUw4ekI5RnFUcUYxOHJu?=
 =?utf-8?B?ZHZkcXVLTTNzbSt5QjVEcUI3U3FQNlVyNjYrSFVGWmZUVWVTTzlmYmwxc3Jh?=
 =?utf-8?B?ZmZkK3BLU2t4SnVMQWxkc0pWQzhhT2R5NVI0amplbW12L0tqc0Z2cndPdDdO?=
 =?utf-8?B?TloyUVF5WjdtOWpobEV5ZGpQT0tFZnhNYkVEQXpadERWK25DU0NLd3RDNWNw?=
 =?utf-8?B?Mm1rVWx5NGJtT1FobTBNQkIzZVJPTzBuV2QzSTZFSmFkdzJ5ZVdsbC9HaCtl?=
 =?utf-8?B?eHpNbFV5RytEejF1VVhNamZJTEpNRHpTSmRQN3MwWENTMkIwdjdvNUFJOUVz?=
 =?utf-8?B?Q3A4aFpJMFYyaENDVUpZUHFZbVRCRk5vSGNjQTBEaU1Dc0ZaQS9zWm1zcGJj?=
 =?utf-8?B?TUIwTnRoZDZUNE8xV0ljenFJUlJQTU43TnV0dGVjQWFzM2ZWemZHZXkzSkZL?=
 =?utf-8?B?MDJ0WloxUTdZYVFkem1taWUrNENOaVkxQ0xYQXM0RzlOaXhrL3piM25jY3p5?=
 =?utf-8?B?UnUyOWJFWEtpc05jUDlQeHkwU1R0TURKY0RhM2ZIdXhrK2xhcFpNb1hxaFc2?=
 =?utf-8?B?SVRmdkF2dlMxMThNODd6S3ozdVMrWlhTQW5ENFd3RjZFQWxJeFc3M0xnTEts?=
 =?utf-8?B?UURBTGNYVlhyVUNsZjV5Q3ZUMTZhUHpmMUV0UkRWejVVbUg3M2FFbmtvN0R0?=
 =?utf-8?B?MGxacmszWjh3RmFkY3UxWjNaNDN0MFptZ3B0UG5OMUd5cHNNeWk5TnhoUVhh?=
 =?utf-8?B?dEpCSkY3WVVkN1dhanZCbTRTWlZRZWpjNXA1cnNoNmxPUXl4Rm5jSDJhMy9D?=
 =?utf-8?B?QWtrQXg4Vm0xL3Y1OEJYWTVJU3BXM0Q4aDlRaXFLOG00bWJTSDRkUmVnQjZy?=
 =?utf-8?B?YWZMYytyUHovaEw4cVZTd3FwRGRsT3ROOUI2WExWVTR1MDBZd25LdDVIbGY3?=
 =?utf-8?B?QytVYlhNOTFZdkpIOTF1TDladnFQeW40aTJka2hlcVpYRExJVjBadXVldDVY?=
 =?utf-8?B?NW9JOStkZ09vWUhyblMxVnhpcko4UGIxcVgxbzJ0Z3c1U0FzaU10bUxkQ2Iz?=
 =?utf-8?B?Z2JTUHlQd0Z4aDNXZTlodnZnTzZjRjJBTC93UUJDSS9uTGdTVGpkanZZT3Nj?=
 =?utf-8?B?Q3Rmamsyaks2czAvNVF3M1lBVzIwZGdMOEJZa2FqV1dLaEJodGtsQ2MyWVpG?=
 =?utf-8?B?QTJmcXYxZ3pIREo4NThvYVllQ05tSTdBeDMwcWVqcHBuNURHM1JBV2x3YURR?=
 =?utf-8?B?d1gwakJ1Z3lkQjhrd2V6MUFrM2d4Q2hQT2tLZ1czN1JWK1hKa2hpc3MvcGdY?=
 =?utf-8?B?VFZ2aEs2cjhsVWV4RHF1UEtBczBHSUFaTkN0c05SYk5LaE90cElFdTh6RFF0?=
 =?utf-8?B?aC8wMlpaNmNyYi9Jc3pRWkZHYWdISXVBcW1TTFMvRENhcCsraGJXY2ZON0JT?=
 =?utf-8?B?a0FXa0ZUK3pIQXJWbkZyRHhMWWNQcTkrSFlERmgyQXFvK3hIRVNlTndyaGNT?=
 =?utf-8?B?bGVQVjBWQkpRY0ptTWJuUHVBVVJ0cnplMEVmbEF0UlRRSytOSFEyUnVGS2tQ?=
 =?utf-8?B?WHVEaXBCdVNzQjZ2RGpBdGNTR1BEQUQ2eXV2N0oyQ3gzVGZvSS9hUT09?=
X-Forefront-Antispam-Report: CIP:209.85.214.171;CTRY:US;LANG:en;SCL:1;SRV:;IPV:NLI;SFV:NSPM;H:mail-pl1-f171.google.com;PTR:mail-pl1-f171.google.com;CAT:NONE;SFS:(13230022)(4636009)(451199015)(336012)(55446002)(1096003)(34756004)(86362001)(8676002)(83380400001)(40140700001)[PHONE-17])(7636003)(42186006)(7596003)(356005)(33964004)(6666004)(53546011)(9686003)(26005);DIR:INB;
X-MS-Exchange-CrossTenant-OriginalArrivalTime: 30 Nov 2022 14:45:49.8184
 (UTC)
X-MS-Exchange-CrossTenant-Network-Message-Id: 2a730d71-15c9-4698-b107-08dad2e192c4
X-MS-Exchange-CrossTenant-Id: 48b0431c-82f6-4ad2-a023-ac96dbf5614e
X-MS-Exchange-CrossTenant-AuthSource: SN1NAM02FT0064.eop-nam02.prod.protection.outlook.com
X-MS-Exchange-CrossTenant-AuthAs: Anonymous
X-MS-Exchange-CrossTenant-FromEntityHeader: Internet
X-MS-Exchange-Transport-CrossTenantHeadersStamped: PH0PR17MB4718
X-OrganizationHeadersPreserved: PH0PR17MB4718.namprd17.prod.outlook.com
X-CrossPremisesHeadersPromoted: wiwpexc01.wbmi.com
X-CrossPremisesHeadersFiltered: wiwpexc01.wbmi.com
X-OriginatorOrg: wbmi.onmicrosoft.com

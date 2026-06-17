---
title: "How Meltdown and Spectre Were Independently Discovered By Four Research Tea"
kind: article
party: third
source: pocket
source_id: "pocket:0170"
provenance: extracted
url: "https://www.wired.com/story/meltdown-spectre-bug-collision-intel-chip-flaw-discovery/"
ingested: 2026-05-13
created: 2018-01-08
tags: [evolution, synchronisity, tech]
status: reference
pocket_status: unread
enrichment: original
---

On cloud computing services like Amazon Web Services, where multiple virtual machines coexist in the same physical server, one malicious virtual machine could peer deeply into the secrets of its neighbors. The Graz team's discovery, an attack that would come to be known as Meltdown, proved a critical crack in one of computing's most basic safeguards. And perhaps most troubling of all, the feature they had exploited was introduced into Intel chips in the mid-1990s. The attack had somehow remained possible, without any apparent public discovery, for decades.
Yet when Intel responded to the trio's warning—after a long week of silence—the company gave them a surprising response. Though Intel was indeed working on a fix, the Graz team wasn't the first to tell the chip giant about the vulnerability. In fact, two other research teams had beaten them to it. Counting another, related technique that would come to be known as Spectre, Intel told the researchers they were actually the fourth to report the new class of attack, all within a period of just months.
"As far as I can tell it’s a crazy coincidence," says Paul Kocher, a well-known security researcher and one of the two people who independently reported the distinct but related Spectre attack to chipmakers. "The two threads have no commonality," he adds. "There’s no reason someone couldn’t have found this years ago instead of today."
Quadruple Collision
In fact, the bizarre confluence of so many disparate researchers making the same discovery of two-decade-old vulnerabilities raises the question of who else might have found the attacks before them—and who might have secretly used them for spying, potentially for years, before this week's revelations and the flood of software fixes from practically every major tech firm that have rushed to contain the threat.
The synchronicity of those processor attack findings, argues security researcher and Harvard Belfer Center fellow Bruce Schneier, represents not just an isolated mystery but a policy lesson: When intelligence agencies like the NSA discover hackable vulnerabilities and exploit them in secret, they can't assume those bugs won't be rediscovered by other hackers in what the security industry calls a "bug collision."
'There’s no reason someone couldn’t have found this years ago instead of today.' Paul Kocher, Cryptography Research
The Meltdown and Spectre incident isn't, after all, the first time major bugs have been found concurrently. Something—and even Schneier admits it's not clear what—leads the world's best security researchers to make near-simultaneous discoveries, just as Leibniz and Newton simultaneously invented calculus in the late 17th century, and five different engineers independently invented the television within years of one another in the 1920s.
"It's weird, right? It’s like there’s something in the water," says Schneier, who last summer co-authored a paper on vulnerability discovery. "Something happens in the community and it leads people to think, let’s look over here. And then they do. And it definitely occurs way more often than chance."
So when the NSA finds a so-called zero-day vulnerability—a previously unknown hackable flaw in software or hardware—Schneier argues that tendency for rediscovery needs to factor into whether the agency stealthily exploits the bug for espionage, or instead reports it to whatever party can fix it. Schneier argues bug collisions like Spectre and Meltdown mean they should err on the side of disclosure: According to rough estimates in the Harvard study he co-authored , as many as one third of all zero-days used in a given year may have first been discovered by the NSA.

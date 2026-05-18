---
title: "https://medium.com/daostack/decentralized-governance-first-principles-1fc6eaa492ed?source=userActivityShare-3a6d69157903-1518258670"
kind: article
party: third
source: pocket
source_id: "pocket:0182"
provenance: extracted
url: "https://medium.com/daostack/decentralized-governance-first-principles-1fc6eaa492ed?source=userActivityShare-3a6d69157903-1518258670"
ingested: 2026-05-13
created: 2018-02-10
tags: []
status: reference
pocket_status: unread
enrichment: original
---

Decentralized Governance Matters Matan Field Follow 6 min read · Feb 6, 2018 -- 10 Listen Share
Blockchain hype is at an all-time high and many people anticipate the first decentralized application to reach the market and gain mass adoption. The term DAO (decentralized autonomous organization) is no longer esoteric. And hundreds of like-minded teams are building decentralized collaborative social news, insurance and investment platforms, numerous collaboration spaces, and even a couple of decentralized autonomous space agencies.
The common element still missing in the above examples is a proper decentralized governance system: an efficient and resilient engine for collective decision-making, at scale. The possibility of thousands, and millions, of people to make decisions together, quickly and wisely.
This is the first blog post in a series on decentralized governance systems, beginning with describing its most basic challenge and the necessary principles to overcome it. In the next post I detail a novel governance model that could efficiently coordinate thousands of cooperating agents. In the third post I present DAOstack: an operating system for collective intelligence and the necessary toolkit for decentralized collaboration, at scale. I will review its architecture and components therein, going live on the Ethereum mainnet in March 2018. In another post I will introduce Alchemy, a first interface to the DAO stack for easy configuration and management of DAOs. Its up-coming MVP is focused around decentralized budgeting for open-source projects.
Blockchain Is a Decentralized Governance System
In preparation for the main subject, note that the blockchain itself is a decentralized governance system, albeit a very specific one. It allows for a large network of computers to continuously agree on certain things every few seconds such as the balance of tokens, and more generally a set of programs and their internal states.
The blockchain achieves a consensus about certain objective realities such as who transacted how much, to whom and when, and is thus an engine for objective consensus. Comparably, a general governance system of human agents can reach a consensus on intersubjective realities, such as the value of a contribution to a collaborative project, the size of an insurance payout, or the quality of an article. It is thus an engine for intersubjective consensus.¹
Yet the blockchain plays a key role in intersubjective consensus engines as well. We need the blockchain to record agents’ inputs, as well as keep the unambiguous conversion rules from input to output (the governance protocol), and most importantly execute them trustlessly.
Moreover, being a governance system by itself, the blockchain faces the universal challenge of collective decision-making, described below, and the corresponding principles to overcome it will be analogous to known principles used in blockchain research.
Natural Tension
Consensus engines suffer from a fundamental challenge known as the “scalability problem” ³:
In any decentralized governance system there is a principal tension between resilience and scalability.
In this context, resilience means the tolerance and even resistance of a governance system to faulty behavior: whether fraudulent or simply due to poor consideration. By scalability we mean the ability of a governance system to process a large number of decisions in a given period, and even increase its rate as more agents participate in the network.
It is easy to understand the origin of this tension. Decentralization of decision-making processes means having a large number of impactful decision makers, or voters. Resilience demands that decisions cannot be hijacked by a small minority; which naturally needs a large fraction of active voters paying attention to each decision in order to avoid that. And scalability, once again, means potentially many decisions to be made at every interval.
However, if each decision needs to be considered by most voters, then the entire organization has the bandwidth of a single agent, and even worse than that, roughly the bandwidth of the slowest one. Which certainly cannot be scalable or produce many good decisions in a short time frame.² This problem simply reflects the natural limit on the bandwidth of collective attention, resulting in the inescapable tension between resilience and scalability.
Basic Principles
The above is a real physical tension. In consensus systems, increasing the threshold for consensus increases resilience but lowers scalability, and vice versa. More decentralization of the process enables more intelligence agents to contribute, potentially increasing capacity and resilience at the same time. However, effective decentralization depends critically on the degree of coherence in the system, and otherwise may reduce them both.
To be specific:
Any resolution of this tension will allow minority decisions (improving on scale) that are guaranteed to be in strong correlation with the majority “truth” (protecting resilience).
This would be our definition of coherence and is a necessary condition for scalable governance.
A few basic principles are available to enable coherence and scalable governance. I introduce them below in broad strokes and will give a detailed example in my next post in this series. We will see that each of these principles is analogous to a known principle in blockchain research.
Monetization of Attention
Human attention, and in particular intelligence, is a scarce resource, and thus has to be represented by a scarce element. In other words, attention has to be monetized: acquiring collective attention on a network of intelligent agents has to be paid for by a valuable token.
This is also the basic economic model behind the blockchain itself and specifically the notion of gas in Ethereum. However, in a decentralized governance system, acquiring attention works differently than paying miners to verify transactions in the blockchain: there is no single voter approving a proposal at a given time analogous to the notion of a successful miner of a block.
Monetization of attention allows a decentralized, wider decision-making process, while protecting it from abuse and maintaining resilience in the network.
Compositionality
Decision-making processes can become more efficient in a more complexly structured system. To demonstrate that, let us consider the comparison between two voting-system modes: an assembly and a confederation. An assembly is a single, flat voting system, with, say, fifteen equal voting agents. Majority decision is achieved with the consent of eight. In a confederation, the same fifteen agents organize into three parties of five equal-vote agents. Each party is a meta-agent with equal voting power within the larger system. There are three ways by which the confederation is superior to the assembly:
The parties can organize around different topics of expertise, and with sufficient trust, the larger group can delegate topical decisions to the smaller parties. On-going decisions can be delegated to the smaller parties by, for example, allocating a limited budget for them to manage locally. Decisions of the entire confederation are made more efficient. A global decision can be approved with the consent of two parties (as two-out-of-three voting agents), which is achievable by the total consent of six basic agents, three from each group, rather than a total of eight. (Note, however, that not just any configuration of six agents works.)
This principle is somewhat reminiscent of blockchain scalability solutions such as sharding, Cosmos, and Polkadot.
Holographic Consensus
Group consensus means that an entire group of agents agrees on something, whatever their rules for agreement may be (e.g., the consent of 50% majority of token holders or 60% of reputation holders). By “holographic consensus” we mean that a deciding group allows any subset, a smaller party within itself, to make decisions on its behalf, under certain conditions. A good holographic consensus guarantees a high degree of coherence, and thus strong correlation of sub-group decisions with the will of the greater majority.
The crux of holographic consensus is having an external staking system in which “auditors” can predict the outcome of incoming proposals. This would be the broader analogue of the off-chain computations paradigm used these days to solve blockchain scalability. In the next post I will introduce this novel holographic-consensus model in detail. We will see how the attention of the collective is drawn to the “interesting proposals” and how the system maintains coherence and remains protected from faulty behavior. In the third post of this series we present DAOstack, an operating system for collective intelligence, a general framework for blockchain governance and crypto-economic incentive systems.
In March 2018, DAOstack launches Alchemy, its first application for decentralized budgeting. Alchemy implements the holographic-consensus protocol designed for scalable and resilient governance, permitting crowd-management of budget for large-scale, open-source projects.
Closing Remarks
Decentralized governance is a critical element for DAOs and DApps. The greatest challenge of distributed consensus is to enable an efficient navigation of the collective attention, effectively charting decision space and picking up the important decisions to have it focused on. Such a mechanism would resolve the tension between excessive output of collective attention on certain things, to achieve greater efficiency; and insufficient collective attention on other things, for the sake of better consensus. Monetization of attention, complexity and coherence are necessary principles to achieve the two goals simultaneously and form a truly scalable governance system, with which thousands of collaborating agents would process hundreds decisions a day, safely.
Join the DAOstack conversation on Telegram or Forum.
—————————————————————————————————
¹ To be fair, the reality of token ownerships is partially intersubjective as well. However, the incoming events influencing those realities are themselves objective.
² In the particular high-frequency case of blockchain, an additional bottleneck of communication speed among agents makes scalability a bigger issue.
³ See, for example: https://github.com/ethereum/wiki/wiki/Sharding-FAQ .

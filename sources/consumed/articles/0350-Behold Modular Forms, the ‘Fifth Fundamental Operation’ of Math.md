---
title: "Behold Modular Forms, the ‘Fifth Fundamental Operation’ of Math"
kind: article
party: third
source: pocket
source_id: "pocket:0350"
provenance: extracted
url: "https://www.quantamagazine.org/behold-modular-forms-the-fifth-fundamental-operation-of-math-20230921/"
ingested: 2026-05-13
created: 2023-09-23
tags: []
status: reference
pocket_status: unread
enrichment: original
---

Two kinds of transformations copy the fundamental domain to the right and left, as well as to a series of ever-shrinking semicircles along the horizontal axis. These copies fill the entire upper half of the complex plane.
A modular form relates the copies to each other in a very particular way. That’s where its symmetries enter the picture.
If you can move from a point in one copy to a point in another through the first kind of transformation — by shifting one unit to the left or right — then the modular form assigns the same value to those two points. Just as the values of the cosine function repeat in intervals of $latex 2\pi$, a modular form is periodic in one-unit intervals.
Meanwhile, you can get from a point in one copy to a point in another through the second type of transformation — by reflecting over the boundary of the circle with radius 1 centered at the origin. In this case, the modular form doesn’t necessarily assign those points the same value. However, the values at the two points relate to each other in a regular way that also gives rise to symmetry.
You can combine these transformations in infinitely many ways, which gives you the infinitely many symmetry conditions that the modular form must satisfy.
“That doesn’t necessarily sound very exciting,” said John Voight, a mathematician at Dartmouth College. “I mean, carving up the upper half-plane and putting numbers on various places — who cares?”
“But they’re very elemental,” he added. And there’s a reason why that’s the case.
Controlled Spaces
In the 1920s and ’30s, the German mathematician Erich Hecke developed a deeper theory around modular forms. Crucially, he realized that they exist in certain spaces — spaces with specific dimensions and other properties. He figured out how to describe these spaces concretely and use them to relate different modular forms to one another.
This realization has driven a lot of 20th- and 21st-century mathematics.
To understand how, first consider an old question: How many ways can you write a given integer as the sum of four squares? There is only one way to write zero, for instance, while there are eight ways to express 1, 24 ways to express 2, and 32 ways to express 3. To study this sequence — 1, 8, 24, 32 and so on — mathematicians encoded it in an infinite sum called a generating function:
$latex 1 + 8q + {{24q}^2} + {{32q}^3} + {{24q}^4} + {{48q}^5} + …$
There wasn’t necessarily a way to know what the coefficient of, say, $latex q^{174}$ should be — that was precisely the question they were trying to answer. But by converting the sequence into a generating function, mathematicians could apply tools from calculus and other fields to infer information about it. They might, for instance, be able to come up with a way to approximate the value of any coefficient.
But it turns out that if the generating function is a modular form, you can do much better: You can get your hands on an exact formula for every coefficient.
“If you know it’s a modular form, then you know everything,” said Jan Bruinier of the Technical University of Darmstadt in Germany.
That’s because the infinitely many symmetries of the modular form aren’t just beautiful to look at — “they’re so constraining,” said Larry Rolen of Vanderbilt University, that they can be made into “a tool for automatically proving congruences and identities between things.”
Mathematicians and physicists often encode questions of interest in generating functions. They might want to count the number of points on special curves, or the number of states in certain physical systems. “If we are lucky, then it is a modular form,” said Claudia Alfes-Neumann, a mathematician at Bielefeld University in Germany. That can be very difficult to prove, but if you can, then “the theory of modular forms is so rich that it gives you tons of possibilities to investigate these [series] coefficients.”
Building Blocks
Any modular form is going to look very complicated. Some of the simplest — which are used as building blocks for other modular forms — are called Eisenstein series.
You can think of an Eisenstein series as an infinite sum of functions. To determine each of those functions, use the points on an infinite 2D grid:

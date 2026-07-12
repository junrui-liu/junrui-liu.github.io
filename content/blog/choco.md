+++
title = "Solver-aided chorale composition"
date = "2022-06-11"
slug = "choco"
tags = [
    "music", "logic"
]
+++

## Introduction
Composing music is hard: if you hit the keys on a piano randomly, chances are, it won't sound great. A music theory aims to distill a musical *syntax* such that a syntactically correct composition will not sound "wrong." Under this view, composition becomes a constraint satisfaction problem: given a background theory, find a sequence of composition actions that does not violate the theory's syntax.

To illustrate this view, here's a toy project called [Choco](https://github.com/junrui-liu/choco) that I built for composing music in the style of [Baroque four-part chorales](https://en.wikipedia.org/wiki/Four-part_harmony). It was originally developed as a course project for [CS 292C - Computer Aided Reasoning for Software](https://github.com/fredfeng/CS292C/tree/spring-2022), and was motivated by my earlier memory of doing four-part voice leading in a music theory class. I felt at that time that the rules of four-part harmony were rigid enough, and the process mechanical enough, that it would be possible to automate the process of composing a chorale. Choco is my attempt at doing just that.

The tool is written in [Rosette](https://emina.github.io/rosette/), a really cool solver-aided programming language [^1] that I've also been using for [my (more serious) research](https://dl.acm.org/doi/10.1145/3503222.3507751).[^2] Note that the idea of algorithmic composition using symbolic reasoning is not new, dating back to at least 1988 with [Ebcioglu's CHORAL project](http://www.global-supercomputing.com/people/kemal.ebcioglu/pdf/Ebcioglu-JLP90.pdf). This toy project showcases how Rosette greatly simplifies the implementation of such a system: we just need to design a simple representation of chorales and write down the rules of four-part harmony as logical predicates in Racket. Rosette then takes a chorale sketch and automatically compiles it into constraints that can be easily solved by an SMT solver. In particular, there is no need to hand-roll a backtracking search algorithm ourselves, and Rosette does not need to have any understanding of music theory to be able to compose music.

## Background

A chorale typically consists of four independent *voices*. Each voice is a sequence of *notes* drawn from a fixed collection known as a *scale*. At each time step, the set of notes across all voices forms a *chord*, and the evolution of chords over time is called a *progression*.

{{< themed-img light="/images/choco-progression-light.png" dark="/images/choco-progression-dark.png" alt="Diagram of a chorale: four voices unfold over time; at each time step the notes across all voices form a chord, and the sequence of chords forms a progression" >}}

## How Choco works

### 1. The user provides a chorale sketch

A sketch is a partial chorale that contains a combination of *concrete* notes and chords, and *symbolic* notes and chords. The concrete elements are what the user already has in mind, while the symbolic elements are holes yet to be filled in to make the composition complete. 

In the sketch below, the user specifies a concrete top voice (the melody they want), while all remaining voices are symbolic. The user also fixes progression's first and last chords using Roman numerals (I and V), while all chords in between are yet-to-be-determined:

{{< themed-img light="/images/choco-sketch-light.png" dark="/images/choco-sketch-dark.png" alt="A chorale sketch: a concrete melody on the top staff, empty lower voices, and a progression reading I, six question marks, V" >}}

### 2. Syntax rules become logical predicates

Choco encodes the syntactic rules of classical harmony as logical predicates over the sketch. For instance:

- (Harmony) Every voice must be in harmony with the current chord: each note must match some [pitch class](https://en.wikipedia.org/wiki/Pitch_class) of the chord.
- (No voice crossing) Voices cannot "cross" each other between adjacent time steps: if one voice sits above another now, it must remain above at the next step.

{{< themed-img light="/images/choco-rules-light.png" dark="/images/choco-rules-dark.png" alt="The two rules as logical predicates: the harmony rule, ∀n ∈ V. ∃pc ∈ C. n ≡ pc, marked with a green check; the voice-crossing rule, ∀n, m ∈ Vₜ × Vₜ₊₁. V(n) < V(m) ⟹ n < m, marked with a red cross" >}}

### 3. Angelic execution fills the sketch

Finally, we ask the solver to fill the holes in a way that satisfies all of the syntax rules simultaneously. In Rosette, this is just two lines of code:

```racket
(define model (solve (assert cs)))
(evaluate sketch model)
```

Given the sketch above (a concrete melody bookended by I and V), Choco fleshes it out into a complete four-voice chorale:

{{< themed-img light="/images/choco-result-light.png" dark="/images/choco-result-dark.png" alt="The completed chorale: all four voices filled in, with the progression I, V⁷/iv, iv⁶₄, V⁶₄, V⁶₅/ii, ii, I, V" >}}

## Optimizations

Naively throwing the constraints at the solver does not scale, so Choco employs a few tricks:

1. Expensive symbolic computations are pre-computed and looked up from a table instead of being re-derived symbolically.
2. The problem is decomposed both *horizontally* (temporally, across time steps) and *vertically* (chordally, across voices), with backtracking to recover when a locally-chosen fragment cannot be extended.
3. Constraints are rewritten to avoid expensive modular-arithmetic operations, which SMT solvers handle poorly.

## Future work

1. Mere syntactical correctness does not imply the music should sound good. In fact, the completed chorale shown above is quite janky-sounding. We might want to frame composition as an *optimal* synthesis problem, to account for soft syntactic constraints (rules that good compositions prefer to follow but may occasionally break), or to bias the search towards more "musical" solutions. 
2. Design a DSL for specifying the syntax of different music genres and theories, so the framework isn't hard-wired to Baroque harmony.
3. Extend the framework to incorporate metric theory and transformational theory.

## References

[^1]: Torlak and Bodik. *A Lightweight Symbolic Virtual Machine for Solver-Aided Host Languages.* PLDI '14.
[^2]: I was also inspired by Cong and Leo's [*Counterpoint by Construction* (FARM '19)](https://dl.acm.org/doi/10.1145/3331543.3342578). There's a similar work which I found out after completing this project: [recreational-rosette/music](https://github.com/kach/recreational-rosette/tree/master/music).

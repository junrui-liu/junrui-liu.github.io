+++
title = "Logic as Minecraft (Part 1)"
date = "2026-07-12"
slug = "mc-logic-1"
tags = [
    "logic"
]
+++

## Introduction

This blog post is intended to be the first in a series where I try out an alternative approach to teaching formal logic and proofs, using a crafting/resource management game as a vehicle. I will be taking liberal inspiration and examples from the wonderful [Minecraft](https://en.wikipedia.org/wiki/Minecraft) video game, a game that I enjoy[^mc].

[^mc]: along with apparently [400 million other people](https://en.wikipedia.org/wiki/Minecraft#Sales)

The reason I wanted to try something new is that, although I've always found logic fascinating, it has a reputation for being quite abstract and challenging in classroom settings. I came up with this Minecraft approach while preparing for a teaching demo talk I gave during my recent academic job interviews, which I had a lot of fun crafting (ha!), and I thought it would be fun to share it here. I hope it'll make learning logic not only *fun and intuitive* through (literal) Minecraft gameplay, but also *interactive* by later incorporating a live coding environment called an [interactive theorem prover](https://en.wikipedia.org/wiki/Proof_assistant)[^itp], which will allow us to play logic as a (surprisingly addictive) game with real-time feedback.

[^itp]: which I've enjoyed using in [my research](https://doi.org/10.1109/SP54263.2024.00078), and which also has tons of potential in making learning CS more engaging---see [this paper](https://dl.acm.org/doi/10.1145/3758317.3759679), for example.


Hopefully, the series is accessible to those who have seen a bit of Boolean logic (like conjunction `∧` and implication `→`), but other than that, no background in formal logic or proof techniques is assumed.[^expert]

[^expert]: Spoiler for those of you who are logic experts: {{< spoiler >}} the underlying logic I will be using is *[intuitionistic](https://en.wikipedia.org/wiki/Intuitionistic_logic) [sequent calculus](https://en.wikipedia.org/wiki/Sequent_calculus)*, rather than (more conventional) [classical](https://en.wikipedia.org/wiki/Classical_logic) [axiomatic logic](https://en.wikipedia.org/wiki/Axiomatic_system) or [natural deduction](https://en.wikipedia.org/wiki/Natural_deduction). Moreover, the presentation will have a strong [linear/substructural logic](https://en.wikipedia.org/wiki/Linear_logic) flavor to it. 
{{< /spoiler >}}
<!-- Those choices are not arbitrary -- towards the end of this series, I will discuss why I think they offer distinct pedagogical benefits in a first-exposure setting. -->
<!-- Linearity enables students to draw upon a wealth of already developed intuition of "making things from resources", and the sequent calculus formalism provides a friendly user interface (UI) for students to interact with. -->
<!-- However, there won't be any mention of sequent calculus will be made in this blog post, and the reader is not expected to have any prior knowledge of it. At the end of the blog post, I will briefly discuss how each concept in the game maps to its counterpart in sequent calculus. -->


Without further ado, let's dive in.

## Ground rules

Let's play a game of **construction**, where we will be *making* or *crafting* things out of other things. It's a game that you have probably played before, in many different contexts:
- If you like cooking or baking, you may have made a dish out of ingredients, e.g., a cake out of flour, sugar, eggs, and butter.
- If you took a chemistry class, you learned that the water molecule (H₂O) can be made out of hydrogen (H₂) and oxygen (O₂).

Keep those intuitions in mind, because they will serve you well in the game we are about to play.

Our game will be played as follows:
- There will be **items** which can be *made*, or *used* to make other items.
- As the game designer, I will prescribe a set of **actions** that combine existing items to make new items.
- At any point in time, the game is in a certain **state**, which consists of an **inventory** of items that we currently have, and a single **goal** item that we are trying to make.
- We **win** the game if we make the goal item. That is, if in the current state, the goal item is right there in our inventory!

We will visualize a game that transitions from one state to another as follows:

{{< mc-derivation >}}
{ "diagram": { "inv": ["A","B","D"], "goal": "G", "rule": "A, B → C", "dir": "fwd",
  "children": [ { "inv": ["C","D"], "goal": "G" } ] } }
{{< /mc-derivation >}}

<!-- Original ASCII (kept for reference):
```
  A                       
  B                     C
  D     (A, B -> C)     D
===== --------------&gt; =====
  G                     G
```
-->
Here's how to read this diagram:
1. Initially on the left, our inventory contains items `A`, `B` and `D`, and we are trying to make item `G`. We will use the horizontal line to separate the inventory from the goal.
2. We then apply the action `A, B -> C`, which consumes items `A` and `B` from our inventory and produces item `C`.
3. After this action, we are now in a new state where our inventory contains item `C`. Both inventory item `D` and goal item `G` remain unaffected by this action.

I haven't told you what the items are and what actions are available to us yet. Let me introduce them now, all inspired by... Minecraft!


## Let's play Minecraft

Here are the only items in our game, for now:
- {{< item "wood" >}}
- {{< item "charcoal" >}}
- {{< item "stick" >}}
- {{< item "ore" >}}
- {{< item "iron" >}}
- {{< item "axe" >}}

The actions we can take are as follows:
1. {{< act "burn" >}}: {{< item "wood" >}} → {{< item "charcoal" >}}
2. {{< act "chop" >}}: {{< item "wood" >}} → {{< item "stick" >}}
3. {{< act "smelt" >}}: {{< item "ore" >}}, {{< item "charcoal" >}} → {{< item "iron" >}}
4. {{< act "assemble" >}}: {{< item "stick" >}}, {{< item "iron" >}} → {{< item "axe" >}}

I hope that even if you haven't played Minecraft before, you can intuitively understand what these actions mean, based on real-world analogies:[^mc-history]
1. {{< act "burn" >}}: You can burn a piece of wood to make charcoal.
2. {{< act "chop" >}}: You can chop a piece of wood to make a stick.
3. {{< act "smelt" >}}: You can smelt a piece of ore with charcoal to make iron.
4. {{< act "assemble" >}}: You can assemble a stick and iron to make an axe.

[^mc-history]: After all, Minecraft is a pretty good simulation of how our ancestors lived in the Middle Ages (at least before you get into the redstone stuff)!

To familiarize ourselves with the game, let's play a few rounds, shall we? Say the initial state of our game is as follows:

{{< mc-derivation step="0" >}}
{ "engine": { "have": ["wood", "ore"], "show": "axe", "script": null } }
{{< /mc-derivation >}}

<!-- Original ASCII (kept for reference):
```
wood
ore
====
axe
```
-->
That is, assume that we already have a piece of `wood` and a piece of `ore` in our inventory, and our goal is to make an `axe`, which is marked with an {{< leaf-tag "open" >}} tag since the goal item is not yet in our inventory.

**Exercise**: Take a pause, and think about how you would play this game. What action would you take first?

---

We might reason like this: "Well, we eventually need an axe, and to make an axe, the {{< act "assemble" >}} action says we need a stick and iron..."

Good! Let's pause right there and focus on the `stick` first. Since we have a piece of `wood`, we can use the {{< act "chop" >}} action to make a `stick`. Let's see that in action by clicking the NEXT button:

{{< mc-derivation step="0" >}}
{ "engine": { "have": ["wood", "ore"], "show": "axe",
  "script": { "rule": "chop" } } }
{{< /mc-derivation >}}

Now, let's focus on the `iron`. To make `iron`, we need to use the {{< act "smelt" >}} action, which requires `ore` and `charcoal`. We already have `ore`, but we don't have `charcoal` yet. How can we get `charcoal`? Well, we can use the {{< act "burn" >}} action on `wood` to make `charcoal`...

Wait, we don't have any `wood` left in our inventory! We just used it to make a `stick`, which means we're technically stuck, unless we started with more `wood` in our inventory.

## Honorable cheating

As a kind game designer, I want to make our life a little easier: let's NOT worry about how many copies of each item we have in our inventory. Instead, I will introduce a "cheat-code" action called {{< act "dup" >}}, whose effect is captured by the following diagram:

{{< mc-derivation step="1" >}}
{ "engine": { "have": ["A", "..."], "show": "G",
  "script": { "rule": "dup", "hints": { "A": "A" } } } }
{{< /mc-derivation >}}

<!-- Original ASCII (kept for reference):
```
                 A
  A              A
 ...            ...
===== -[dup]-> =====
 ...            ...
```
-->
That is, for any item `A`, {{< act "dup" >}} allows us to make a copy of `A` in our inventory.

Intuitively, what this cheat code says is that *possessing one copy of an item is as good as having infinitely many copies of that item*. In other words, we don't have to worry about running out of items in our inventory, since we can always keep duplicating them.[^dup] [^nocheat]

[^dup]: If you are familiar with Minecraft, {{< act "dup" >}} might remind you of the differences between ["survival mode" and "creative mode"](https://www.minecraft.net/en-us/article/creative-vs-survival-mode): in survival mode, you can't duplicate items; in creative mode, you can not only duplicate items, but you can also create items out of thin air. In our game, without {{< act "dup" >}}, the game is played exactly like Minecraft's survival mode; with {{< act "dup" >}}, the game sits somewhere in between survival and creative modes, since we can duplicate items, but we can't create them out of thin air.

[^nocheat]: In case you'd rather play without this cheat code, that's totally valid too, giving you a different "mode" of the game, one that we'll probably come back to at the very end of this blog post.
For now, though, let's assume {{< act "dup" >}} is available, since we'll have more interesting stuff to worry about than inventory management!

I also want to bring your attention to another interesting aspect of this action, which differs from the other four actions ({{< act "burn" >}}, {{< act "chop" >}}, {{< act "smelt" >}}, {{< act "assemble" >}}) in an important way: the item `A` involved in the action is *generic*. That is, item `A` is just a placeholder for any item in our game. We can specialize {{< act "dup" >}} to duplicate wood, charcoal, iron, and so on, by replacing the generic placeholder `A` with a specific item (as long as the thing we are duplicating is *already* in our inventory). Heck, the exact name of the placeholder `A` is not important, and we could have named it `X` or `FireInTheHole`. In contrast, the other four actions are *specific* to the items involved in them. For example, {{< act "burn" >}} is specific to `wood` and `charcoal`, and we can't use it to burn `ore` into `iron`. 


We will follow the convention that placeholders are capital letters `A`, `B`, `C`, etc., while specific items are lowercase letters like `wood`, `charcoal`, `stick`, etc.

---

With our new cheat code in hand, we can now finish our previous game! 

Recall that the reason we couldn't fully make an axe before was that we needed *two* pieces of wood (one for the stick, and one for the charcoal to help smelt iron), but we started with only one. Let's just use {{< act "dup" >}} on `wood`, after which we play the game as before:

{{< mc-derivation step="1" >}}
{ "engine": { "have": ["wood", "ore"], "show": "axe",
  "script": { "rule": "dup", "hints": { "A": "wood" }, "children": [ { "rule": "chop", "children": [ { "rule": "burn", "children": [ { "rule": "smelt", "children": [ { "rule": "assemble" } ] } ] } ] } ] } } }
{{< /mc-derivation >}}

<!-- Original ASCII (kept for reference):
```
                 wood              stick             stick
wood             wood              wood              charcoal           stick                 
ore              ore               ore               ore                iron                  axe
======= -[dup]-> ======= -[chop]-> ======= -[burn]-> ======= -[smelt]-> ======= -[assemble]-> =======
axe              axe               axe               axe                axe                   axe
```
-->
In the last state, the goal item `axe` is in our inventory, so we have successfully completed the game. Nice.

## Alternative thinking

You may have noticed that how the game state evolves in the above diagram runs counter to the way we initially reasoned about the game (and arguably the more "natural" way of thinking). Previously, our reasoning started with the eventual goal item `axe`, and we worked **backwards** to figure out what we needed to make it (namely, a `stick` and `iron`); then we recursively broke down those "sub-goals" to figure out further items we need.

But when we actually played the game by drawing the state transition diagram, we started with the items in our inventory in the *initial state* (namely, `wood` and `ore`) and reasoned **forward** to figure out what we could make with them, eventually leading us to the goal item `axe`.

Forward reasoning means that we always focus on what's *above* the line---items we already have. When reasoning forward, we always have the risk of making something that we don't need eventually, or spending a resource that we should have saved for something else, meaning we always have to cross our fingers and pray that we're indeed making progress.

Instead, can we shift our focus onto what's *below* the line---our ultimate goal---and progressively decompose it into smaller sub-goals that are hopefully easier to tackle? This way, we know that every step we take is a step that we must take towards our ultimate goal, and we won't waste any resources on things that don't help us get there.

This is indeed possible. **Backward reasoning** is a very effective strategy that complements forward reasoning. In backward reasoning, we always focus on the goal item and ask ourselves: "What do we need to achieve this goal?" Then we recursively break down the sub-goals until we reach items that are already in our inventory.

Let's instead apply backward reasoning to play the same game. The initial state of the game is the same as before:

{{< mc-derivation >}}
{ "diagram": { "inv": ["wood","ore"], "goal": "axe" } }
{{< /mc-derivation >}}

<!-- Original ASCII (kept for reference):
```
wood         
ore          
======= 
axe
```
-->
This time, we simply ignore the inventory part, instead focusing on the goal item `axe`. We ask ourselves: "What do we need to make an axe?" The answer is given by the {{< act "assemble" >}} action: we need a `stick` and `iron`, which means we can decompose our goal into two sub-goals: make a `stick` and make `iron`. Let's write that down:

{{< mc-derivation >}}
{ "diagram": { "inv": ["wood","ore"], "goal": "axe", "rule": "assemble", "dir": "bwd",
  "children": [ { "inv": ["?1"], "goal": "stick" }, { "inv": ["?2"], "goal": "iron" } ] } }
{{< /mc-derivation >}}

<!-- Original ASCII (kept for reference):
```
                       ?1
wood                   =====
ore                  / stick
======= <-[assemble]-
axe                  \ ?2
                       =====
                       iron
```
-->
You see, using backward reasoning, the diagram is no longer a linear sequence: the initial state is "forked" into two independent branches, one for each sub-goal. We will tackle each sub-goal separately, which may further fork into more sub-goals, and so on. Our diagram will eventually grow into a **tree**, whose root, the initial state, is on the left and the tree grows towards the right. (Note that we also switch the direction of the arrow to indicate that we are applying the {{< act "assemble" >}} action right-to-left.)

In the backward setting, a subtle yet important question arises: what should the inventories of the branches be (marked `?1` and `?2` in the diagram above)? In other words, when we fork the game state into two branches, how should we manage the inventory?

Note that this question is a *game design question*, since it will affect all games that involve backward reasoning and hence potentially affect every player.

## Inventory management

The most natural approach that you might think of is to "split" the inventory into two disjoint parts, one for each branch. For example, we might allocate `wood` to the left branch and `ore` to the right branch, which would give us the following diagram:

{{< mc-derivation >}}
{ "diagram": { "inv": ["wood","ore"], "goal": "axe", "rule": "assemble", "dir": "bwd",
  "children": [ { "inv": ["wood"], "goal": "stick" }, { "inv": ["ore"], "goal": "iron" } ] } }
{{< /mc-derivation >}}

Intuitively, this makes sense. The meaning of our initial state is that an `axe` must be made from items in the initial inventory; since `axe` can be made from `stick` and `iron`, some of the items in the initial inventory must be used to make `stick`, and the rest must be used to make `iron`; hence it seems natural to split the inventory into two disjoint parts, one for each branch.

Let's call this approach to inventory management the **split inventory** design. There is absolutely nothing wrong with this approach[^linear]. It's just one of the many ways to design the game. That said, this approach makes the game more difficult to play, because we must correctly predict which items to allocate to each branch, often before we can know which items will actually be needed.

To see this, let's look at the previous diagram. If we try to continue the game, we will quickly discover that the game is stuck for exactly the same reason as before: the lower branch needs another piece of `wood` to make `charcoal` for smelting `iron`, but the upper branch already used up the only piece of `wood` in the inventory to make a `stick`. Thus, we would have to backtrack, insert a {{< act "dup" >}} action to duplicate `wood`, and then have the foresight to allocate one piece of `wood` to the upper branch and the other piece of `wood` to the lower branch:


{{< mc-derivation >}}
{ "diagram": { "inv": ["wood","ore"], "goal": "axe", "rule": "dup", "dir": "fwd",
  "children": [ { "inv": ["wood","wood","ore"], "goal": "axe", "rule": "assemble", "dir": "bwd",
    "children": [ { "inv": ["wood"], "goal": "stick" }, { "inv": ["wood","ore"], "goal": "iron" } ] } ] } }
{{< /mc-derivation >}}

<!-- Original ASCII (kept for reference):
```                      
                 wood                   wood     
wood             wood                   =====
ore              ore                  / stick
======= -[dup]-> ====== <-[assemble]-
axe              axe                  \ wood
                                        ore
                                        =====
                                        iron
```
--->

[^linear]: It turns out that there are actual logics that are based on this idea of splitting the inventory into disjoint parts, for example, [linear logics](https://en.wikipedia.org/wiki/Linear_logic).

Correctly managing the inventory can get more challenging as our goal becomes more complex and the game tree has to grow deep as a result. In those cases, we need some serious foresight and advanced planning to make sure we're allocating the right items to the correct branches.

To make our life easier, though, I argue that {{< act "dup" >}} actually allows us to *simplify* our inventory management approach: instead of carefully splitting the inventory into two disjoint parts, we are justified in allowing *each branch to inherit the same inventory as the original state*. For example, the following diagram illustrates another valid way to manage the inventory, where both branches inherit `wood` and `ore`:
   
{{< mc-derivation step="1" >}}
{ "engine": { "have": ["wood", "ore"], "show": "axe",
  "script": { "rule": "assemble", "dir": "bwd", "children": [ ] } } }
{{< /mc-derivation >}}

   <!-- Original ASCII (kept for reference):
   ```
                            wood
                            ore
   wood                     =====
   ore                    / stick
   =======   <-[assemble]-
   axe                    \ wood
                            ore
                            =====
                            iron
   ```
   --->

Let's call this alternative approach the **inherited inventory** design. I argue that this design is also justified. Essentially, the two designs are essentially equivalent in their expressive power: if a player can win the game under one design, then they can also win the game under the other design.

Specifically, a game-tree diagram played under the inherited inventory design is just a collapsed version of some other diagram under the split inventory design: in the former diagram, we are just hiding some of the {{< act "dup" >}} actions that we would have had to explicitly insert in the latter diagram. For example, we can think of the above diagram as a collapsed version of the following diagram, where we explicitly inserted {{< act "dup" >}} actions to duplicate `wood` and `ore` before forking the game state:

{{< mc-derivation >}}
{ "diagram": { "inv": ["wood","ore"], "goal": "axe", "rule": "dup", "dir": "fwd",
  "children": [ { "inv": ["wood","wood","ore"], "goal": "axe", "rule": "dup", "dir": "fwd",
    "children": [ { "inv": ["wood","wood","ore","ore"], "goal": "axe", "rule": "assemble", "dir": "bwd",
      "children": [ { "inv": ["wood","ore"], "goal": "stick" }, { "inv": ["wood","ore"], "goal": "iron" } ] } ] } ] } }
{{< /mc-derivation >}}

The inherited inventory design has one important advantage: it arguably makes the game easier to play and is more "forgiving", because it saves us from having to plan ahead and explicitly write out {{< act "dup" >}} actions. Instead, we just duplicate *every* item so that it becomes available to all branches for the rest of the game. If we happen to need that item down the road, then great; if we don't, then no harm done, since possessing unused items can never lose us the game.

Therefore, we will assume the inherited inventory design for the rest of this blog series, as it makes the lives of the players easier.


**Exercise**: Can you play the game using backward reasoning under the inherited inventory design, i.e., without using any explicit {{< act "dup" >}} actions?


{{< mc-derivation >}}
{ "diagram": { "inv": ["wood","ore"], "goal": "axe" } }
{{< /mc-derivation >}}

<details>
<summary>Click to reveal the solution</summary>

{{< mc-derivation step="0" >}}
{ "engine": { "have": ["wood", "ore"], "show": "axe",
  "script": { "rule": "assemble", "dir": "bwd", "children": [
    { "rule": "chop", "dir": "bwd" },
    { "rule": "smelt", "dir": "bwd", "children": [ null, { "rule": "burn", "dir": "bwd" } ] } ] } } }
{{< /mc-derivation >}}

</details>

## Back and forth

In summary, here's how backward reasoning works more generally:

> If we have an action {{< act "f" >}}: `A, B -> C`, and our current goal is to make `C`, then we can apply {{< act "f" >}} backwards to fork the game state into two branches, one whose goal is `A` and one whose goal is `B`. The inventory of each branch is identical to the original inventory.

Diagrammatically, we can represent backward reasoning as follows:

{{< mc-derivation >}}
{ "diagram": { "inv": ["?1"], "goal": "C", "rule": "f", "dir": "bwd",
  "children": [ { "inv": ["?1"], "goal": "A" }, { "inv": ["?1"], "goal": "B" } ] } }
{{< /mc-derivation >}}

<!-- Original ASCII (kept for reference):
```
              ?1
              ====
?1          / A
==== <-[f]-
C           \ ?1
              ====
              B
```
-->
Importantly, each branch inherits the *same* inventory (`?1`) as the original state, following the inherited inventory design, because we don't want to worry about inserting {{< act "dup" >}} actions at the right places all the time, which also makes the diagram much cleaner and easier to read.

Let's also compare backward reasoning to the forward reasoning diagram:

{{< mc-derivation >}}
{ "diagram": { "inv": ["A","B"], "goal": "G", "rule": "f", "dir": "fwd",
  "children": [ { "inv": ["C"], "goal": "G" } ] } }
{{< /mc-derivation >}}

<!-- Original ASCII (kept for reference):
```
A
B           C
==== -[f]-> ====
??          ??
```
-->

The following slogans help us remember the difference between forward and backward reasoning:
> Forward reasoning looks at the ***inventory*** (what we have).
> 
> Backward reasoning looks at the ***goal*** (what we want).

**Exercise**: Can you complete the following game using a *mix* of forward and backward reasoning? Is there an order of mixing forward and backward reasoning that takes the fewest number of actions? Is there an order that you find the most intuitive?


{{< mc-derivation >}}
{ "diagram": { "inv": ["wood","ore"], "goal": "axe" } }
{{< /mc-derivation >}}

<!-- {{< mc-derivation step="0" >}}
{ "engine": { "have": ["wood", "ore"], "show": "axe",
  "script": { "rule": "assemble", "dir": "bwd", "children": [
    { "rule": "chop", "dir": "bwd" },
    { "rule": "smelt", "dir": "bwd", "children": [ null, { "rule": "burn", "dir": "bwd" } ] } ] } } }
{{< /mc-derivation >}} -->

<!-- Original ASCII (kept for reference):
```
                       wood
                       ore
wood                   ===== <-[?]- ...
ore                  / stick
======= <-[assemble]-
axe                  \ wood
                       ore
                       ===== <-[?]- ...
                       iron
```
-->


## Whew!

That was a lot of ground covered. We learned the rules of a game of construction and two different ways of playing it: forward and backward.

Next up, we will introduce new designs to the game to make it a LOT more interesting, making a truly "open-world" game. Our new designs will allow a player to create arbitrarily complex contraptions that even the game designer might not have anticipated. Importantly, though, we will see that what we have been building all along is---believe it or not---logic[^gotcha]!

[^gotcha]: Bet you already forgot about that!

+++
title = "Logic as Minecraft (Part 1)"
date = "2026-07-07"
slug = "mc-logic-1"
tags = [
    "logic"
]
+++



This blog post is intended to be the first in a series where I try out an alternative approach to teaching formal logic and proofs, using a crafting/resource management game as a vehicle. I will be taking liberal inspiration and examples from the wonderful [Minecraft](https://en.wikipedia.org/wiki/Minecraft) video game, a game that I enjoy [^mc].

[^mc]: along with apparently [400 million other people](https://en.wikipedia.org/wiki/Minecraft#Sales)

The reason I wanted to try something new is that, although I've always found logic fascinating, it has a reputation for being quite abstract and challenging in classroom settings. I came up with this Minecraft approach while preparing for a teaching demo talk I gave during my recent academic job interviews, which I had a lot of fun crafting (ha!). So I thought it would be fun to share it here. I hope it'll make learning logic not only *fun and intuitive* through (literal) Minecraft gameplay, but also *interactive* by later incorporating a live coding environment called an [interactive theorem prover](https://en.wikipedia.org/wiki/Proof_assistant) [^itp], which will allow us to play logic as a (surprisingly addictive) game with real-time feedback.

[^itp]: which I've been enjoying using in [my research](https://doi.org/10.1109/SP54263.2024.00078), and which also has tons of potential in making learning CS more engaging---see [this paper](https://dl.acm.org/doi/10.1145/3758317.3759679), for example.


Hopefully, the series is accessible to those who have seen a bit of Boolean logic (like conjunction `∧` and implication `→`), but other than that, no background in formal logic or proof techniques is assumed.
[^expert]

[^expert]: Spoiler for those of you who are logic experts: {{< spoiler >}} the underlying logic I will be using is *[intuitionistic](https://en.wikipedia.org/wiki/Intuitionistic_logic) [sequent calculus](https://en.wikipedia.org/wiki/Sequent_calculus)*, rather than (more conventional) [classical](https://en.wikipedia.org/wiki/Classical_logic) [axiomatic logic](https://en.wikipedia.org/wiki/Axiomatic_system) or [natural deduction](https://en.wikipedia.org/wiki/Natural_deduction). Moreover, the presentation will have a strong [linear/substructural logic](https://en.wikipedia.org/wiki/Linear_logic) flavor to it. 
{{< /spoiler >}}
<!-- Those choices are not arbitrary -- towards the end of this series, I will discuss why I think they offer distinct pedagogical benefits in a first-exposure setting. -->
<!-- Linearity enables students to draw upon a wealth of already developed intuition of "making things from resources", and the sequent calculus formalism provides a friendly user interface (UI) for students to interact with. -->
<!-- However, there won't be any mention of sequent calculus will be made in this blog post, and the reader is not expected to have any prior knowledge of it. At the end of the blog post, I will briefly discuss how each concept in the game maps to its counterpart in sequent calculus. -->


Without further ado, let's dive in!

## Ground rules

Let's play a game: a game of **construction**, where we will be *making* or *crafting* things out of other things. It's a game that you have probably played before, in many different contexts:
- If you like cooking or baking, you may have made a dish out of ingredients, e.g., a cake out of flour, sugar, eggs, and butter.
- If you took a chemistry class, you learned that the water molecule (H₂O) can be made out of hydrogen (H₂) and oxygen (O₂).
- If you have played Minecraft, you most likely crafted an iron axe out of a wooden stick and iron.

Keep those intuitions in mind, because they will serve you well in the game we are about to play.

Our game will be played as follows:
- There will be **items** which can be *made*, or *used* to make other items.
- As the game designer, I will prescribe a set of **actions** that you can use to combine existing items to make new items.
- At any point in time, the game is in a certain **state**, which consists of an **inventory** of items that you currently have, and a single **goal** item that you are trying to make.
- You **win** the game if you make the goal item. That is, if in the current state, the goal item is right there in your inventory!

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

I haven't told you what the items are and what actions are available to us. In fact, this is where the game designer gets to be creative and have lots of fun. 

For now, I will role-play as the game designer, and you will role-play as the player: I will tell you what items are available and what actions you can take, and your job is to figure out how to make the goal item from the items in your inventory. Once you become more comfortable with the game, you'll get a chance to role-play as game designers! How cool is that?

So let me introduce you to the items and the actions in our game, which are all inspired by... Minecraft!


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

To familiarize ourselves with the game, let's play a few rounds, shall we? Let's say the initial state of our game is as follows:

{{< mc-derivation >}}
{ "diagram": { "inv": ["wood","ore"], "goal": "axe" } }
{{< /mc-derivation >}}

<!-- Original ASCII (kept for reference):
```
wood
ore
====
axe
```
-->
That is, let's say we already have a piece of wood and a piece of ore in our inventory, and our goal is to make an axe.

**Exercise**: Take a pause, and think about how you would play this game. What action would you take first?

---

We might reason like this: "Well, we eventually need an axe, and to make an axe, the {{< act "assemble" >}} action says we need a stick and iron..."

Good! Let's pause right here and focus on the `stick` first. Since we have a piece of `wood`, we can use the {{< act "chop" >}} action to make a `stick`. Let's do that:

{{< mc-derivation step="0" >}}
{ "engine": { "have": ["wood", "ore"], "show": "axe",
  "script": { "rule": "chop" } } }
{{< /mc-derivation >}}

Now, let's focus on the `iron`. To make `iron`, we need to use the {{< act "smelt" >}} action, which requires `ore` and `charcoal`. We already have `ore`, but we don't have `charcoal` yet. How can we get `charcoal`? Well, we can use the {{< act "burn" >}} action on `wood` to make `charcoal`...

Wait, we don't have any `wood` left in our inventory! We just used it to make a `stick`. So technically, we're stuck, unless we started with more `wood` in our inventory. 



## Honorable cheating

As a kind game designer, I want to make our life a little easier: let's NOT worry about how many copies of each item we have in our inventory. Instead, I will introduce a "cheat-code" action called {{< act "dup" >}}, whose effect is captured by the following diagram:

{{< mc-derivation >}}
{ "diagram": { "inv": ["A","…"], "goal": "…", "rule": "dup", "dir": "fwd",
  "children": [ { "inv": ["A","A","…"], "goal": "…" } ] } }
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

[^nocheat]: In case you don't like this cheat code and want to play the game without it, that's totally valid! That'll give you a slightly different "mode" that makes it different from the "base game" which assumes {{< act "dup" >}}. In fact, the game mode without {{< act "dup" >}} will lead us to some fascinating discussions about the nature of logic and proofs and to the discovery of non-standard logics. We'll touch on that at the very end of this blog post.
But for now, let's assume we play in a mode where {{< act "dup" >}} is available, since we'll have more interesting stuff to worry about than inventory management!

I also want to bring your attention to another interesting aspect of this action, which differs from the other four actions ({{< act "burn" >}}, {{< act "chop" >}}, {{< act "smelt" >}}, {{< act "assemble" >}}) in an important way: the item `A` involved in the action is *generic*. That is, item `A` is just a placeholder for any item in our game. We can specialize {{< act "dup" >}} to duplicate wood, charcoal, iron, and so on, by replacing the generic placeholder `A` with a specific item (as long as the thing we are duplicating is *already* in our inventory). Heck, the exact name of the placeholder `A` is not important, and we could have named it `X` or `FireInTheHole`. In contrast, the other four actions are *specific* to the items involved in them. For example, {{< act "burn" >}} is specific to `wood` and `charcoal`, and we can't use it to burn `ore` into `iron`. 


We will follow the convention that placeholders are capital letters `A`, `B`, `C`, etc., while specific items are lowercase letters like `wood`, `charcoal`, `stick`, etc.

---

With our new cheat code in hand, we can now finish our previous game! 

Recall that the reason we couldn't fully make an axe before was that we needed *two* pieces of wood (one for the stick, and one for the charcoal to help smelt iron), but we started with only one. So let's just use {{< act "dup" >}} on `wood`, after which we play the game as before:

{{< mc-derivation step="0" >}}
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
In the last state, the goal item `axe` is in our inventory, so we have successfully completed the game! Hooray!



## Alternative thinking

You may have noticed that how the game state evolves in the above diagram runs counter to the way we initially reasoned about the game (and arguably the more "natural" way of thinking): previously, our reasoning started with the eventual goal item `axe`, and we worked backwards to figure out what we needed to make it (namely, a `stick` and `iron`); then we recursively broke down those "sub-goals" to figure out further items we need.

But when we actually played the game by drawing the state transition diagram, we started with the items in our inventory in the *initial state* (namely, `wood` and `ore`) and applied **forward reasoning** to figure out what we could make with them, eventually leading us to the goal item `axe`.

Forward reasoning means that we always focus on what's *above* the line -- items we already have. When reasoning forward, we always have the risk of making something that we don't need eventually, or spending a resource that we should have saved for something else. So we always have to cross our fingers and pray that we're indeed making progress.

Instead, can we shift our focus onto what's *below* the line---our ultimate goal---and progressively decompose it into smaller sub-goals that are hopefully easier to tackle? This way, we know that every step we take is a step that we must take towards our ultimate goal, and we won't waste any resources on things that don't help us get there.

Indeed, this is possible! In fact, **backward reasoning** is a very effective strategy that complements forward reasoning. In backward reasoning, we always focus on the goal item and ask ourselves: "What do we need to make this item?" Then we recursively break down the sub-goals until we reach items that are already in our inventory.

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
This time, we simply ignore the inventory part, instead focusing on the goal item `axe`. We ask ourselves: "What do we need to make an axe?" The answer is given by the {{< act "assemble" >}} action: we need a `stick` and `iron`. So we can decompose our goal into two sub-goals: make a `stick` and make `iron`. Let's write that down:

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
You see, using backward reasoning, the diagram is no longer a linear sequence: the initial state is "forked" into two independent sub-states, one for each sub-goal. For each sub-goal, we will tackle them separately, which may further fork into more sub-goals, and so on. So our diagram will eventually grow into a tree. (Note that we also switch the direction of the arrow to indicate that we are applying the {{< act "assemble" >}} action right-to-left.)


With backward reasoning, a new and important question arises: what should the inventories of the sub-states be (marked `?1` and `?2` in the diagram above)? In other words, when we fork the game state into two sub-states, how should we manage the inventory? 

This is a non-trivial and non-obvious question, one that perhaps only a game designer can answer, since deciding how inventory behaves under backward reasoning affects *all* actions applied backwards. Different design choices will lead to different gaming experiences for the player. Some might make the game harder, some might make it easier---hey, even the designer might not know for sure until tons of people have played through it!  This is what I think the real thrill of this series is: seeing how a seemingly innocent design choice can have far-reaching and emergent effects on the game and the player's experience.

<!-- [^game-logic]: Spoiler: the game we're designing is actually a logical system. So the design choices we'll explore literally change the kind of logical reasoning that's allowed. -->

Let's experience this first-hand by exploring different designs of inventory management under backward reasoning.

## Designing inventory management

**Open-ended exercise**: I encourage you to pause and think about what design(s) immediately occur to you, and then pretend to be a player and try to play the game under your design(s).

Sadly, since a blog is a non-interactive medium, I can't explore your ideas with you together, and will have to read your mind and anticipate several reasonable designs you might propose (see if I guessed right!):
1. **Clean split**: Whatever `?1` and `?2` are, their *union* should be the original inventory, but they should be *disjoint* -- that is, `?1` and `?2` should not have any items in common.
     - For example, take `?1 = wood` and `?2 = ore`. Then they cleanly split the original inventory into two disjoint parts.
2. **Overlapping split**: The union of `?1` and `?2` should be the original inventory, but they don't have to be disjoint.
      - For example, take `?1 = wood` and `?2 = wood, ore`, so they share `wood` in common, an overlap forbidden by design 1 but allowed here. The union of `?1` and `?2` is still the original inventory. 
3. **Total overlap**: Both `?1` and `?2` are *identical* to the original inventory. I.e., the diagram simply looks like this:

   {{< mc-derivation >}}
   { "diagram": { "inv": ["wood","ore"], "goal": "axe", "rule": "assemble", "dir": "bwd",
     "children": [ { "inv": ["wood","ore"], "goal": "stick" }, { "inv": ["wood","ore"], "goal": "iron" } ] } }
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
   -->


**Exercise**: Take a pause here. Which design makes more sense to you? Can you explain why in a sentence or two?

*Hint*: there is no single "correct" answer. Which design lets you finish the game, and which design will get you stuck? If more than one design lets you finish the game, which one is more "efficient" in terms of the total number of actions you need to take? 

---

Ok. Perhaps you have come up with your own answer and reasoning. If not, that's fine! At least you gave it some serious thought, which is what matters.

Let's think through the three designs together. I claim that design 1 is probably the most "natural" choice at first glance. Here's a plausible explanation. Let's say our current state has items `A` through `E`, and the goal is to make `Z`, which comes from the action `X, Y -> Z` (or, if you read it backwards, `Z <- X, Y`):

{{< mc-derivation >}}
{ "diagram": { "inv": ["A","B","C","D","E"], "goal": "Z", "rule": "X, Y → Z", "dir": "bwd",
  "children": [ { "inv": ["…"], "goal": "X" }, { "inv": ["…"], "goal": "Y" } ] } }
{{< /mc-derivation >}}

<!-- Original ASCII (kept for reference):
```
A
B          ...
C          ====
D           X
E        /
==== <---
Z        \
           ...
           ====
            Y
```
-->
which means that however smart we are and whatever path the game takes, `X` must ultimately be made from `A` through `E`, right?

Now, because we are reasoning backwards, we need to first use the same set of resources (`A`-`E`) to produce `X` and `Y`, independently. So our initial resources must be divided, some of which will be used to make `X`, and the rest of which will be used to make `Y`. The former items will be in the inventory for the upper branch, and the latter items will be in the inventory for the lower branch.

Back to our original example:

{{< mc-derivation >}}
{ "diagram": { "inv": ["wood","ore"], "goal": "axe", "rule": "assemble", "dir": "bwd",
  "children": [ { "inv": ["?1"], "goal": "stick" }, { "inv": ["?2"], "goal": "iron" } ] } }
{{< /mc-derivation >}}

It is therefore natural to require that `?1` and `?2` are disjoint, and their union is the original inventory: some of the original items go into `?1`, and the rest go into `?2`. This is design 1.

Unfortunately, design 1 might sometimes get us stuck...

**Exercise**: Take a pause. Why will we get stuck under design 1? You can use our previous game as an example:


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

---

Well, we run into the same problem as before: both `stick` and `iron` require `wood` to make.

- If we allocate `wood` to `?1` for `stick`, then we won't have any `wood` left to make `iron`.
- If we allocate `wood` to `?2` to make `iron`, then we won't have any `wood` left to make `stick`.
In either case, we can't finish the game.

So if we were to pick design 1, we would need to insert a {{< act "dup" >}} action to duplicate `wood` prior to {{< act "assemble" >}}:

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
-->
If we did this, then all is well.

In fact, the presense of `dup` is exactly why design 2 is *also* a reasonable design choice!

Recall that, thanks to {{< act "dup" >}}, having one copy of an item in our inventory is (spiritually) just as good as having infinitely many copies of that item. So we can justify copying the same item, say `wood`, into both `?1` and `?2` in the diagram, because we could have easily applied {{< act "dup" >}} before {{< act "assemble" >}} to duplicate `wood` like the diagram above shows. In other words, design 2 is no more powerful than design 1; it just saves us from having to explicitly write out {{< act "dup" >}} actions. 

Another way to think about design 2 is that, if we can finish a game under design 2, there's an equivalent way to finish the game under design 1: take the game tree for winning under design 2, and just insert a bunch of {{< act "dup" >}} actions at the right places (i.e., on the items that are implicitly duplicated in a backward-applied action).

For example, the following diagram assumes design 2, where `wood` is implicitly duplicated into both `?1` and `?2`:

{{< mc-derivation >}}
{ "diagram": { "inv": ["wood","ore"], "goal": "axe", "rule": "assemble", "dir": "bwd",
  "children": [ { "inv": ["wood"], "goal": "stick" }, { "inv": ["wood","ore"], "goal": "iron" } ] } }
{{< /mc-derivation >}}

<!-- Original ASCII (kept for reference):
```
                       wood
wood                   =====
ore                  / stick
======= <-[assemble]-
axe                  \ wood
                       ore
                       =====
                       iron
```
-->
But we could have also explicitly written out the {{< act "dup" >}} action, which was exactly what we had to do under design 1:

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
-->
So, design 2 = design 1 + some implicit {{< act "dup" >}}'s that we're too lazy to write out.

If this makes sense to you, then I hope it would not be too difficult to generalize design 2 to design 3: instead of implicitly duplicating *some* items in the original inventory, we can implicitly duplicate *all* items in the original inventory:

{{< mc-derivation >}}
{ "engine": { "have": ["wood", "ore"], "show": "axe",
  "script": { "rule": "assemble", "dir": "bwd" } } }
{{< /mc-derivation >}}

<!-- Original ASCII (kept for reference):
```
                       wood
                       ore
wood                   =====
ore                  / stick
======= <-[assemble]-
axe                  \ wood
                       ore
                       =====
                       iron
```
-->
This makes inventory management a non-issue! We don't even need to think about which items to duplicate at each "fork". In fact, it may be very difficult to predict which items to duplicate at a fork, since an item may be *evantually* needed at two different places very deep in the game tree.

So design 3 gives us the peace of mind: just copy everything in the original inventory to each branch. If we ever need the extra copies, great! Otherwise, we can just ignore any unused copies. For example, in the diagram above, we technically don't *need* to duplicate `ore` into the upper branch, but it doesn't hurt to do so.

Because design 3 renders the problem inventory management moot, we will assume it from now on.

**Exercise**: Can you play the game using backward reasoning under design 3, without using any explicit {{< act "dup" >}} actions?


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

In summary, here's how the backward reasoning strategy works more generally:

> If we have an action {{< act "f" >}}: `A, B -> C`, and our current goal is to make `C`, then we can apply {{< act "f" >}} backwards to fork the game state into two sub-states, one whose goal is `A` and one whose goal is `B`. The inventory of each sub-state is identical to the original inventory.

Diagrammatically, we can write this as follows:

{{< mc-derivation >}}
{ "diagram": { "inv": ["??"], "goal": "C", "rule": "f", "dir": "bwd",
  "children": [ { "inv": ["??"], "goal": "A" }, { "inv": ["??"], "goal": "B" } ] } }
{{< /mc-derivation >}}

<!-- Original ASCII (kept for reference):
```
              ??
              ====
??          / A
==== <-[f]-
C           \ ??
              ====
              B
```
-->
Importantly, each sub-state inherits the same inventory (`??`) as the original state (design 3), because we don't want to worry about inserting {{< act "dup" >}} actions at the right places all the time, which also makes the diagram much cleaner and easier to read.

Let's also compare backward reasoning to the forward reasoning diagram:

{{< mc-derivation >}}
{ "diagram": { "inv": ["A","B"], "goal": "??", "rule": "f", "dir": "fwd",
  "children": [ { "inv": ["C"], "goal": "??" } ] } }
{{< /mc-derivation >}}

<!-- Original ASCII (kept for reference):
```
A
B           C
==== -[f]-> ====
??          ??
```
-->

The following slogan helps us remember the difference between forward and backward reasoning:
> Forward reasoning looks at the ***inventory*** (what we have).
> 
> Backward reasoning looks at the ***goal*** (what we want).

**Exercise**: Can you complete the following game using a *mix* of forward and backward reasoning. Is there an order of mixing forward and backward reasoning that takes the fewest number of actions? Is there an order that you find the most intuitive?


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

That was a lot of ground covered. We learned the rules of a game of construction and two different ways of playing it: forward and backward. We not only played a few rounds but also got to think like game designers ourselves.

Next up, we will introduce new designs to the game to make it a LOT more interesting, making a truly "open-world" game. Our new designs will allow a player to create arbitrarily complex contraptions that even the game designer might not have anticipated. Importantly, though, we will see that what we have been building all along is---believe it or not---logic[^gotcha]!

[^gotcha]: Bet you already forgot about that!

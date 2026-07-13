
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

-->
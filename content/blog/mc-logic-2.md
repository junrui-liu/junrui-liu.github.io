
+++
title = "Logic as Minecraft (Part 2)"
date = "2100-07-07"
slug = "mc-logic-2"
tags = [
    "logic"
]
+++

## New item: bundles

Let's make the game a little more interesting by introducing a new item called a **bundle**. If you've been to Costco, where seemingly everything is sold in 2-packs, then you already have a good intuition for what a bundle is: [^vanilla]

{{< slide-row >}}
{{< slide-img src="https://bfasset.costco-static.com/U447IH35/as/smmpx78cjpvtkft6k6x8xnh/4000141950-847__1?auto=webp&format=jpg" alt="Costco 2-pack Oral-B electric toothbrushes" width=300 >}}
or
{{< slide-img src="https://bfasset.costco-static.com/U447IH35/as/37tntwhg2hb5g4zxvmw8zsk/617686-847__1?auto=webp&format=jpg" alt="Costco 2-pack Refill Hand Soap" width=300 >}}
or
{{< slide-img src="https://www.narcity.com/media-library/club-house-artificial-vanilla-extract-bottles-in-a-two-pack-at-costco.jpg?id=50901316" alt="Costco 2-pack Artificial Vanilla Extract" width=300 >}}
{{< /slide-row >}}

[^vanilla]: I'm genuinely curious who needs two oversized bottles of artificial vanilla extract.


Anyway, a **bundle** is a new item that we can make in our game. Given two items `A` and `B`, we can create a bundle containing both `A` and `B`, and we will denote this bundle as `A ⋈ B`.[^bowtie]

[^bowtie]: The symbol `⋈` is intended to evoke the image of using a piece of string to tie two items together into a bundle. 

Note that `A ⋈ B` is a single, composite item, and it is distinct from both `A` and `B`. We call `A` and `B` the **components** of the bundle, which don't have to be the same item.

**Exercise**: Are the following items valid?
1. `iron ⋈ stick`
2. `⋈ charcoal`
3. `wood ⋈ iron ⋈ axe`

<details>
<summary>Click to see the answer</summary>

1. Yes, `iron ⋈ stick` is a valid bundle with two components: `iron` and `stick`.
2. No, `⋈ charcoal` is not a valid bundle because it has only one component on the right. The left component is missing, and "nothing" is not a valid item. A bundle must have exactly two valid items as components, one on the left and one on the right of the `⋈` symbol.
3. This one is a bit tricky. `wood ⋈ iron ⋈ axe` is, in fact, invalid, because it is *ambiguous*:
   - is it `wood ⋈ (iron ⋈ axe)`, which is a valid bundle with two components, `wood` and the nested bundle `(iron ⋈ axe)`, or 
   - is it `(wood ⋈ iron) ⋈ axe`, which is also a valid bundle consisting of a nested bundle `(wood ⋈ iron)` and `axe`?
   
   Without parentheses, we can't determine the intended structure. So we will consider `wood ⋈ iron ⋈ axe` to be an invalid bundle, and require proper grouping with parentheses to clarify the intended structure of the bundle, at least for now.

</details>

---

Now that we have a new kind of item, let's define some actions for interacting with it. This is where we get to role-play as the game designer again!

Of course, there are infinitely many ways we could design permissible actions on bundles, but we will try to be principled about it. We will follow the following simple recipe: for every new composite item we introduce, we will define two actions:
- one where the composite item occurs in the inventory, and
- one where the composite item occurs in the goal.

That's it! It might take a bit of thinking to appreciate why this recipe works. Indeed, any item can only occur in one of two places: either in the inventory or in the goal. So if we define an action for each of these two cases, we have fully specified how to interact with said item.


Let's apply this recipe to design actions for bundles. Remember, we have two cases to consider: when a bundle occurs in the inventory, and when a bundle occurs in the goal.
1. If the bundle, let's say `A ⋈ B`, occurs in the inventory, then we can break it apart into its two components `A` and `B`. We will call this action **[destruct]**:
     ``` 
                          A
     A ⋈ B                B
     ===== -[destruct]-> =====
      ?                   ?
     ```
2. If the bundle occurs in the goal, that means we want to make a bundle, say `A ⋈ B`. Since a bundle consists of two components, `A`, and `B`, we need to make both of them. We will call this action **[construct]**:
     ```
                            ??
                            ====
      ??                  /  A
     ===== <-[construct]-
     A ⋈ B                \ ??
                            ====
                             B
     ```

Note the direction of the arrows in the two diagrams above. In the first diagram, we are applying **[destruct]** in the *forward* direction, because we are breaking apart an existing bundle that we already possess ("forward action reasons from the inventory"). In the second diagram, we are applying **[construct]** in the *backward* direction, because we are trying to make a new bundle that we don't yet possess ("backward action reasons from the goal").

Another way I like to think about the two actions associated with any composite item (not just bundles) is to view one action as a *consumer* and the other as a *producer*: **[destruct]** is a consumer action since it uses up a bundle in the inventory, while **[construct]** is a producer action since it creates a new bundle in the goal.

---

With the game rules for bundles in place, we can now play a new game!
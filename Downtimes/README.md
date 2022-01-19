## !downtime
`!downtime` is an alias that currently works for all 2 or 3 check downtimes and use of it looks like: `!downtime <type> <DC> [arguments]` 

#### Types:
*academic, banditry, crime, gather, herd, horse, hunt, piracy, street*

#### DC:
*Sets the DC for the checks*

### Optional Arguments:
- **`adv`**     *gives **advantage** to __all__ rolls in the downtime*
   - *You can use `adv1`, `adv2`, `adv3` to specify only certain rolls have `adv`*
- **`dis`**     *gives **disadvantage** to __all__ rolls in the downtime*
   - *You can use `dis1`, `dis2`, `dis3` to specify only certain rolls have `dis`*
- **`guid`**   *adds a **guidance** roll to be added to one downtime roll* 
- **`ls`**        *adds the **+1** from the **Luckstone** item to the tool check*  
- **`prof`**  *overwrites `!tool`'s **proficiency** to any tool check in the downtime*  
- **`exp`**     *overwrites `!tool`'s **expertise** to any tool check in the downtime*

## !guild
`!guild` is used to register your guild which is currently used to calculate material cost discount automatically for `!downtime craft` and use of it looks like:  
`!guild -name <guild name> -rank <guild rank> -role <your role>`

#### For example:
`!guild -name "The Order of the Cobalt Quill" -rank 1 -role "an Owner"`

#### It can be only partial though, for example:
`!guild -name cobalt`

### Optional Arguments:
`-name`|`-guild`  
> if multiple words put these little guys around them `""`  

`-rank`  
> Only put a number here like `2` or `3`  

`-role`|`-title`  
> This wants you to put both the job role and an appropriate article such as "the Owner" or "a member"  

## !beloved
This is a two part alias, part one sets up the counter and modifies it, part two uses the counter once  

`!beloved set <#>` *will set up the counter for you or update your counter and automatically caps at proficiency bonus*  

`!beloved` *will expend one use of Beloved Inspiration.*  

### Using the beloved snippet
On any command that uses snippets you can use the beloved snippet to spend the counter, note this snippet does not tell it to roll adv, you must still use the adv snippet, which looks like this:  
`!c stealth beloved adv` or `!s con beloved adv`

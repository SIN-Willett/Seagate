[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/D1D71UZEM)
# Seagate
Aliases, Gvars and all that good stuff for Seagate

## !beloved
This is a two part alias, part one sets up the counter and modifies it, part two uses the counter once  

`!beloved set <#>` *will set up the counter for you or update your counter and automatically caps at proficiency bonus*  

`!beloved` *will expend one use of Beloved Inspiration.*  

### Using the beloved snippet
On any command that uses snippets you can use the beloved snippet to spend the counter, note this snippet does not tell it to roll adv, you must still use the adv snippet, which looks like this:  
`!c stealth beloved adv` or `!s con beloved adv`

## !housing

*This one is pretty self explanatory and had no extra frills, just rolls the d4 from housing benefit.*

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

## !bft

*This is an alias for Bloodfury Tattoo that works with the Blood Thirsty Strikes snippet `bts`*

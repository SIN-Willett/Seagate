[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/D1D71UZEM)
## !downtime work
`!downtime work` is an alias that currently works in conjunction with `!work` and it looks like:  
`!downtime work [arguments]`  

#### For example:
`!downtime work adv guid prof`  
`!downtime work adv exp ls`  
`!downtime work dis`  

### Optional Arguments:

- **`adv`** *gives **advantage***  
- **`dis`**     *gives **disadvantage***
- **`guid`**   *adds **guidance***
- **`ls`**        *adds the **+1** from the **Luckstone** item to the tool check*
- **`prof`**  *overwrites `!tool`'s **proficiency** to the tool check*
- **`exp`**     *overwrites `!tool`'s **expertise** to the tool check*
  
## !work

`!work` is used to register your work for `!downtime work` and use of it looks like:  
`!work -check <check> -income <income> -role <role> -location <location>`  

#### For example:
`!work -check smith -income 5 -role "the Owner" -location "the Greyforge"`  

It can be only partial though, for example:  
`!work -check smith`

### Optional Arguments:
`-check`|`-tool`  
> any full or partial skill or tool should work

`-location`|`-loc`  
> if multiple words put these little guys around them `""`

`-income`|`-inc`|`-wage`  
> Only put a number here like `2` or `3`

`-role`|`-job`  

> This wants you to put both the job role and an appropriate article such as `"the Owner"` or `"an employee"`

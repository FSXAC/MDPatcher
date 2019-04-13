# MDPatcher

v0.1

Script that fixes/patches Markdown files

There is no way I'm going to sift through my hundreds of school notes Markdown files to fix formatting. This script will bulk edit all of them

## Features

### Front Matter

- Always generate front matter for organization and auto-generation purposes.
- Has option to update the document date to the current date
- (TODO): define categories via arguments
- Auto generate title from heading

### Fix Math Block Formatting

- Ensure that inline LaTeX is using double dollar signs (`$x$` &rarr; `$$x$$`)
- Ensure that LaTeX blocks always have non-text line before and after the block
  ```markdown
  <!-- before -->
  Text
  $$
  c^2=x^2+y^2
  $$
  Text
  ```
  ```markdown
  <!--after-->
  Text
  
  $$
  c^2=x^2+y^2
  $$
  
  Text
  ```
- Ensure that above also works in blockquotes
  ```markdown
  <!-- before -->
  > Text
  > $$
  > c^2=x^2+y^2
  > $$
  
  > Text
  ```
  ```markdown
  <!--after-->
  > Text
  >
  > $$
  > c^2=x^2+y^2
  > $$
  >
  > Text
  ```
  
### Use Uniform TOC Option

- Change `[TOC]` to `- toc {:toc}` from Kramdown for easier publishing
- (TODO) make this customizable

### Fix Bad Headings

- Bad headings are like `###Heading 3`, this inserts a space so it's standard like `### Heading 3`

### Fix LaTeX Math Stuff

- I realized that I can't use `|x|` because Markdown compilers like Kramdown will interpret that as a table even if it's encapsulated in a LaTeX tag. This converts `|` (only inside LaTeX tags) to `\vert`.
- (TODO) other stuff could be easily added

## Usage

Use with Python 3+

**Example**


```shell
python fix_markdown.py sample.md
```

Output to a different file:
```shell
python fix_markdown.py sample.md -o sample_out.md
```

Edit all the files in a directory:
```shell
python fix_markdown.py ./notes/
```

Update file with current date:
```shell
python fix_markdown.py sample. --update-date
```

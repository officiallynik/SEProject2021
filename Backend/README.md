# PyStackBot

[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](http://forthebadge.com)


PyStackBot is a StackOverFlow answer summarizer for automated/manually generated queries in vscode for python developers. 


# Table of contents

- [Usage](#usage)
- [API Documentation](#api)
- [Installation](#installation)
- [Resources](#resources)
- [Contributing](#contributing)


# Usage

[(Back to top)](#table-of-contents)

Go to AnswerSearch Directory. Then run the below command
 ```bash
    python3 main.py
 ```
A command line interface for using our tool is shown.
Follow below given rules for searching your query in the given CLI.

- To view the answer summary of the your query, just enter your query on the CLI.
   ![image](https://user-images.githubusercontent.com/17109060/32149062-4f0547ca-bd25-11e7-98b6-587467379704.png)
- Use --q flag to also view the relevant questions that were chosen.
   ![image](https://user-images.githubusercontent.com/17109060/32149062-4f0547ca-bd25-11e7-98b6-587467379704.png)


# Installation

[(Back to top)](#table-of-contents)

1. Run the below command to install the required packages.
  ```bash
    pip3 install -R ./AnswerSearch/requirements.txt
  ```
2. Download all the files given in [this drive link](https://drive.google.com/drive/u/0/folders/1WmS67_kypdYC6gCuK2MYif1a-gJX3TDE). 
   Place the files in the given directories.
   - questions_data.csv   -> Backend/AnswerSearch/Data (Create a new directory in AnswerSearch Directory)
   - answers_data_new.csv -> Backend/AnswerSearch/Data
   - corpus.txt           -> Backend/AnswerSearch/Word2Vec
   - word2vec.model       -> Backend/AnswerSearch/Word2Vec
   - word2vec.model.trainables.syn1neg.npy -> Backend/AnswerSearch/Word2Vec
   - word2vec.model.wv.vectors.npy -> Backend/AnswerSearch/Word2Vec
   - idf.csv ->-> Backend/AnswerSearch/IDF
4. Install the patched fonts of powerline nerd-font and/or font-awesome. Have a look at the [Nerd Font README](https://github.com/ryanoasis/nerd-fonts/blob/master/readme.md) for more installation instructions.

    *Note for `iTerm2` users - Please enable the Nerd Font at iTerm2 > Preferences > Profiles > Text > Non-ASCII font > Hack Regular Nerd Font Complete.*

    *Note for `HyperJS` users - Please add `"Hack Nerd Font"` Font as an option to `fontFamily` in your `~/.hyper.js` file.*

3. Install the [colorls](https://rubygems.org/gems/colorls/) ruby gem with `gem install colorls`

    *Note for `rbenv` users - In case of load error when using `lc`, please try the below patch.*

    ```sh
    rbenv rehash
    rehash
    ```

4. Enable tab completion for flags by entering following line to your shell configuration file (`~/.bashrc` or `~/.zshrc`) :
    ```bash
    source $(dirname $(gem which colorls))/tab_complete.sh
    ```

5. Start using `colorls` :tada:

6. Have a look at [Recommended configurations](#recommended-configurations) and [Custom configurations](#custom-configurations).

# Recommended configurations

[(Back to top)](#table-of-contents)

1. To add some short command (say, `lc`) with some flag options (say, `-l`, `-A`, `--sd`) by default, add this to your shell configuration file (`~/.bashrc`, `~/.zshrc`, etc.) :
    ```sh
    alias lc='colorls -lA --sd'
    ```

2. For changing the icon(s) to other unicode icons of choice (select icons from [here](https://nerdfonts.com/)), change the YAML files in a text editor of your choice (say, `subl`)

    ```sh
    subl $(dirname $(gem which colorls))/yaml
    ```

# Custom configurations

[(Back to top)](#table-of-contents)

You can overwrite the existing icons and colors mapping by copying the yaml files from `$(dirname $(gem which colorls))/yaml` into `~/.config/colorls`, and changing them.

- To overwrite color mapping :

  Please have a look at the [list of supported color names](https://github.com/sickill/rainbow#color-list). You may also use a color hex code as long as it is quoted within the YAML file and prefaced with a `#` symbol.

  Let's say that you're using the dark color scheme and would like to change the color of untracked file (`??`) in the `--git-status` flag to yellow. Copy the defaut `dark_colors.yaml` and change it.

  ```sh
  cp $(dirname $(gem which colorls))/yaml/dark_colors.yaml ~/.config/colorls/dark_colors.yaml`
  ```

  In the `~/.config/colorls/dark_colors.yaml` file, change the color set for `untracked` from `darkorange` to `yellow`, and save the change.

  ```
  untracked: yellow
  ```

  Or, using hex color codes:

  ```
  untracked: '#FFFF00'
  ```

- To overwrite icon mapping :

  Please have a look at the [list of supported icons](https://nerdfonts.com/). Let's say you want to add an icon for swift files. Copy the default `files.yaml` and change it.

  ```sh
  cp $(dirname $(gem which colorls))/yaml/files.yaml ~/.config/colorls/files.yaml`
  ```

  In the `~/.config/colorls/files.yaml` file, add a new icon / change an existing icon, and save the change.


  ```
  swift: "\uF179"
  ```

- User contributed alias configurations :

  - [@rjhilgefort](https://gist.github.com/rjhilgefort/51ea47dd91bcd90cd6d9b3b199188c16)


# Updating

[(Back to top)](#table-of-contents)

Want to update to the latest version of `colorls`?

```sh
gem update colorls
```

# Uninstallation

[(Back to top)](#table-of-contents)

Want to uninstall and revert back to the old style? No issues (sob). Please feel free to open an issue regarding how we can enhance `colorls`.

```sh
gem uninstall colorls
```

# Contributing

[(Back to top)](#table-of-contents)

Your contributions are always welcome! Please have a look at the [contribution guidelines](CONTRIBUTING.md) first. :tada:

# License

[(Back to top)](#table-of-contents)


The MIT License (MIT) 2017 - [Athitya Kumar](https://github.com/athityakumar/). Please have a look at the [LICENSE.md](LICENSE.md) for more details.

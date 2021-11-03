# csme
Conversational State Machine Engine - A language learning CLI tool for visualising and traversing a conversation in multiple languages.


Intended to be, at the core, a simple state machine representing progression through a simple 
conversation. The primary purpose being for language learning / memorisation (Arabic, in my case).

## Features

- Generate PNG conversation diagrams 
- Traverse conversations interactively with the user via STDIN.
- Model supports conversations in multiple languages or scripts over the same "conversation space" (set of valid states)

## Usage

```
rowan:csme$ poetry run python csme --help
Usage: csme [OPTIONS] COMMAND [ARGS]...

  Conversational State Machine Engine.

  A language learning CLI tool for visualising and traversing a conversation
  in multiple languages.

Options:
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.

  --help                          Show this message and exit.

Commands:
  example-json      Print an example conversation set JSON object
  render            Render the input conversation, with states, to PNG
  render-no-states  Render the input conversation, excluding states, to PNG
  run               Traverse the conversation interactively with the user
```

The sample conversation at `data/arabic_1.json` can be used:
```
rowan:csme$ poetry run python csme render data/arabic_1.json
INFO:root:Rendering conversation...
Output filepath: build/ArabicConversation1.png
```

For conversation traversal the user should refer to the generated diagram and enter valid statements ("transitions") as prompted:
```
rowan:csme$ poetry run python csme run data/arabic_1.json
INFO:root:Running CSME service...
INFO:root:case_ignore_filter_enabled: True
INFO:root:Running engine...
Salam
: Marhaba
Masmok?
: Esmi Rowan
INFO:root:Name: Rowan
Maasalama
: Maasalama
```

Run tests:
```
rowan:csme$ poetry run pytest tests/
```



## Future enhancements

- Rename to _Conversation State Machine (CSM)_ or something with [Dialogue System](https://en.wikipedia.org/wiki/Dialogue_system) in the name?
- Look into [transitions extensions](https://github.com/pytransitions/transitions#-extensions) (there's a Diagrams/graphviz one!)
- Add different interfaces:
  - Web - e.g. using [dagre-d3](https://github.com/dagrejs/dagre-d3)
- Add different state machine "traverser" implementations:
  - One using [klaam](https://github.com/ARBML/klaam). Could use speech-to-text and respond with text-to-speech! 
  - Add fuzzy input interpretation
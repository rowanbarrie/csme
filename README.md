# csme
Conversational State Machine Engine

### TODO: Rename to _Conversation State Machine (CSM)_ or something with [Dialogue System](https://en.wikipedia.org/wiki/Dialogue_system) in the name?


Intended to be, at the core, a simple state machine representing progression through a simple 
conversation. The primary purpose being for language learning / memorisation (Arabic, in my case).

## Usage

- TODO: Complete me!

```
poetry run python csme render data/arabic_1.json
```


## Future enchancements


- Look into [transitions extensions](https://github.com/pytransitions/transitions#-extensions) (there's a Diagrams/graphviz one!!)
- Add different interfaces:
  - CLI
  - Web - e.g. using [dagre-d3](https://github.com/dagrejs/dagre-d3)
- Add different state machine "traverser" implementations:
  - CLI-based traverser
  - One using [klaam](https://github.com/ARBML/klaam). Could use speech-to-text and respond with text-to-speech! 

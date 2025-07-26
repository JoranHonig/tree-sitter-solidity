download solidity canonical grammar and identify updates

read last_grammar_version.json 

download current grammar using curl https://raw.githubusercontent.com/ethereum/solidity/blob/develop/docs/grammar/SolidityParser.g4 to file SolidityParser.new.g4

download last grammar using curl https://raw.githubusercontent.com/ethereum/solidity/blob/v{version}/docs/grammar/SolidityParser.g4 to file SolidityParser.new.g4

run `diff SolidityParser.new.g4 SolidityParser.old.g4`

make a list of all grammar rules that changed, describe how they changed and store this in grammar_updates.md
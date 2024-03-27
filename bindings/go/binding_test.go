package tree_sitter_solidity_test

import (
	"testing"

	tree_sitter "github.com/smacker/go-tree-sitter"
	"github.com/tree-sitter/tree-sitter-solidity"
)

func TestCanLoadGrammar(t *testing.T) {
	language := tree_sitter.NewLanguage(tree_sitter_solidity.Language())
	if language == nil {
		t.Errorf("Error loading Solidity grammar")
	}
}

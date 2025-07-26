# Solidity Grammar Updates

## Comparison: v0.8.25 → develop branch

The following grammar rules have changed between version 0.8.25 and the current develop branch:

### 1. **contractDefinition** - Layout Support Added

**Old (v0.8.25):**
```antlr
contractDefinition:
    Abstract? Contract name=identifier
    inheritanceSpecifierList?
    LBrace contractBodyElement* RBrace;
```

**New (develop):**
```antlr
contractDefinition
locals [boolean layoutSet=false, boolean inheritanceSet=false]
:
    Abstract? Contract name=identifier
    (
        {!$layoutSet}? Layout At expression {$layoutSet = true;}
        | {!$inheritanceSet}? inheritanceSpecifierList {$inheritanceSet = true;}
    )*
    LBrace contractBodyElement* RBrace;
```

**Change Description:** Added support for layout specifications in contract definitions. Contracts can now specify a layout using `Layout At expression` syntax. This adds new local variables to track whether layout and inheritance have been set, ensuring they can only be specified once each.

### 2. **enumDefinition** - Formatting Fix

**Old (v0.8.25):**
```antlr
enumDefinition: Enum name=identifier LBrace enumValues+=identifier (Comma enumValues+=identifier)* RBrace;
```

**New (develop):**
```antlr
enumDefinition: Enum name=identifier LBrace enumValues+=identifier (Comma enumValues+=identifier)* RBrace;
```

**Change Description:** Minor formatting change - removed extra tab character before the rule definition.

### 3. **stateVariableDeclaration** - Transient Storage Support

**Old (v0.8.25):**
```antlr
locals [boolean constantnessSet = false, boolean visibilitySet = false, boolean overrideSpecifierSet = false]
```

**New (develop):**
```antlr
locals [boolean constantnessSet = false, boolean visibilitySet = false, boolean overrideSpecifierSet = false, boolean locationSet = false]
```

**Additional clause added:**
```antlr
| {!$locationSet}? Transient {$locationSet = true;}
```

**Change Description:** Added support for transient storage variables. State variables can now be declared with the `transient` keyword, which creates transient storage that is cleared at the end of each transaction.

### 4. **FunctionCallOptions** - Syntax Strictness

**Old (v0.8.25):**
```antlr
| expression LBrace (namedArgument (Comma namedArgument)*)? RBrace # FunctionCallOptions
```

**New (develop):**
```antlr
| expression LBrace (namedArgument (Comma namedArgument)*) RBrace # FunctionCallOptions
```

**Change Description:** Made named arguments in function call options non-optional. The previous version allowed empty braces `{}`, but now at least one named argument is required.

### 5. **PrimaryExpression** - Formatting Fix

**Old (v0.8.25):**
```antlr
 | (
```

**New (develop):**
```antlr
| (
```

**Change Description:** Minor formatting change - removed extra leading space.

### 6. **identifier** - New Keywords as Identifiers

**Old (v0.8.25):**
```antlr
identifier: Identifier | From | Error | Revert | Global;
```

**New (develop):**
```antlr
identifier: Identifier | From | Error | Revert | Global | Transient | Layout | At;
```

**Change Description:** Added three new keywords that can be used as identifiers: `Transient`, `Layout`, and `At`. This supports the new transient storage and layout features while maintaining backward compatibility.

## Summary

The main functional changes are:
1. **Layout Support**: Contracts can now specify memory layouts using `Layout At expression` syntax
2. **Transient Storage**: State variables can be declared as `transient` for transaction-scoped storage
3. **Stricter Function Call Options**: Function call options with braces now require at least one named argument

These changes appear to be part of ongoing Solidity language enhancements, adding new storage types and contract layout capabilities.
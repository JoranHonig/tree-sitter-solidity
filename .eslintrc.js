module.exports = {
  env: {
    commonjs: true,
    es2021: true,
  },
  extends: ['eslint:recommended'],
  globals: {
    grammar: 'readonly',
    seq: 'readonly',
    repeat: 'readonly',
    choice: 'readonly',
    prec: 'readonly',
    optional: 'readonly',
    field: 'readonly',
    token: 'readonly',
    repeat1: 'readonly',
    alias: 'readonly',
  },
  overrides: [
    {
      env: {
        node: true,
      },
      files: ['.eslintrc.{js,cjs}'],
      parserOptions: {
        sourceType: 'script',
      },
    },
  ],
  parserOptions: {
    ecmaVersion: 'latest',
  },
  rules: {
    indent: ['error', 2],
    'linebreak-style': ['error', 'unix'],
    quotes: ['error', 'single', { avoidEscape: true }],
    semi: ['error', 'never'],
  },
}

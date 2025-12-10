import js from '@eslint/js';
import { FlatCompat, } from '@eslint/eslintrc';
import stylisticEslintPlugin from '@stylistic/eslint-plugin';
import { defineConfig, globalIgnores, } from 'eslint/config';
import eslintPluginImport from 'eslint-plugin-import';
import eslintPluginPreferArrow from 'eslint-plugin-prefer-arrow';
import eslintPluginReact from 'eslint-plugin-react';
import eslintPluginUnicorn from 'eslint-plugin-unicorn';
import globals from 'globals';
import path from 'path';
import tseslint from 'typescript-eslint';
import { fileURLToPath, } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const compat = new FlatCompat({
    baseDirectory            : __dirname,
    resolvePluginsRelativeTo : __dirname,
});

export default defineConfig([
    globalIgnores([
        'dist/**',
    ]),
    {
        extends         : [
            js.configs.recommended,
            tseslint.configs.recommended,
            eslintPluginReact.configs.flat.recommended,
            ...compat.extends('plugin:eslint-plugin-react-hooks/recommended'),
        ],
        files           : [
            'src/**/*.{ts,tsx}',
        ],
        languageOptions : {
            ecmaVersion   : 2020,
            globals       : globals.browser,
            parser        : tseslint.parser,
            parserOptions : {
                projectService  : true,
                tsconfigRootDir : import.meta.dirname,
            },
        },
        plugins         : {
            '@typescript-eslint' : tseslint.plugin,
            import               : eslintPluginImport,
            react                : eslintPluginReact,
            'prefer-arrow'       : eslintPluginPreferArrow,
            stylistic            : stylisticEslintPlugin,
            unicorn              : eslintPluginUnicorn,
        },
        settings        : {
            react : {
                version : 'detect',
            },
        },
        rules           : {
            '@typescript-eslint/adjacent-overload-signatures'   : 'error',
            '@typescript-eslint/array-type'                     : [
                'error',
                {
                    'default' : 'array',
                },
            ],
            '@typescript-eslint/ban-ts-comment'                 : 'off',
            '@typescript-eslint/consistent-type-assertions'     : 'error',
            '@typescript-eslint/dot-notation'                   : 'error',
            '@typescript-eslint/explicit-function-return-type'  : 'off',
            '@typescript-eslint/explicit-module-boundary-types' : 'off',
            '@typescript-eslint/no-empty-function'              : 'off',
            '@typescript-eslint/no-empty-interface'             : 'off',
            '@typescript-eslint/no-empty-object-type'           : 'error',
            '@typescript-eslint/no-explicit-any'                : 'off',
            '@typescript-eslint/no-misused-new'                 : 'error',
            '@typescript-eslint/no-misused-promises'            : [
                'error',
                {
                    checksVoidReturn : false,
                },
            ],
            '@typescript-eslint/no-namespace'                   : 'error',
            '@typescript-eslint/no-non-null-assertion'          : 'off',
            '@typescript-eslint/no-parameter-properties'        : 'off',
            '@typescript-eslint/no-shadow'                      : [
                'error',
                {
                    hoist : 'all',
                },
            ],
            '@typescript-eslint/no-unsafe-argument'             : 'off',
            '@typescript-eslint/no-unsafe-assignment'           : 'off',
            '@typescript-eslint/no-unsafe-call'                 : 'off',
            '@typescript-eslint/no-unsafe-function-type'        : 'error',
            '@typescript-eslint/no-unused-expressions'          : 'error',
            '@typescript-eslint/no-unsafe-member-access'        : 'off',
            '@typescript-eslint/no-unsafe-return'               : 'off',
            '@typescript-eslint/no-use-before-define'           : 'error',
            '@typescript-eslint/no-var-requires'                : 'off',
            '@typescript-eslint/no-wrapper-object-types'        : 'error',
            '@typescript-eslint/prefer-for-of'                  : 'error',
            '@typescript-eslint/prefer-function-type'           : 'error',
            '@typescript-eslint/prefer-namespace-keyword'       : 'error',
            '@typescript-eslint/triple-slash-reference'         : [
                'error',
                {
                    path  : 'always',
                    types : 'prefer-import',
                    lib   : 'always',
                },
            ],
            '@typescript-eslint/typedef'                        : 'off',
            '@typescript-eslint/unified-signatures'             : 'error',
            'arrow-body-style'                                  : 'error',
            'comma-dangle'                                      : [
                'error',
                {
                    arrays    : 'always',
                    objects   : 'always',
                    imports   : 'always',
                    exports   : 'always',
                    functions : 'never',
                },
            ],
            complexity                                          : [
                'error',
                {
                    max : 60,
                },
            ],
            'constructor-super'                                 : 'error',
            'default-case'                                      : 'error',
            'dot-notation'                                      : 'error',
            'eol-last'                                          : 'error',
            eqeqeq                                              : [
                'error',
                'smart',
            ],
            'import/order'                                      : 'error',
            'guard-for-in'                                      : 'error',
            'id-denylist'                                       : [
                'error',
                'any',
                'Number',
                'number',
                'String',
                'string',
                'boolean',
                'Undefined',
                'undefined',
            ],
            'id-match'                                          : 'error',
            'linebreak-style'                                   : [
                'error',
                'unix',
            ],
            'max-classes-per-file'                              : [
                'error',
                1,
            ],
            'max-lines'                                         : [
                'error',
                500,
            ],
            'new-parens'                                        : 'error',
            'no-bitwise'                                        : 'off',
            'no-caller'                                         : 'error',
            'no-cond-assign'                                    : 'error',
            'no-console'                                        : 'off',
            'no-debugger'                                       : 'error',
            'no-duplicate-case'                                 : 'error',
            'no-duplicate-imports'                              : 'error',
            'no-empty'                                          : 'off',
            'no-empty-function'                                 : 'off',
            'no-eval'                                           : 'error',
            'no-extra-boolean-cast'                             : 'off',
            'no-fallthrough'                                    : 'off',
            'no-invalid-this'                                   : 'off',
            'no-irregular-whitespace'                           : 'error',
            'no-multiple-empty-lines'                           : 'error',
            'no-new-wrappers'                                   : 'error',
            'no-param-reassign'                                 : 'error',
            'no-redeclare'                                      : 'error',
            'no-shadow'                                         : 'error',
            'no-throw-literal'                                  : 'error',
            'no-trailing-spaces'                                : 'error',
            'no-undef-init'                                     : 'error',
            'no-underscore-dangle'                              : 'off',
            'no-unsafe-finally'                                 : 'error',
            'no-unused-expressions'                             : 'error',
            'no-unused-labels'                                  : 'error',
            'no-use-before-define'                              : 'off',
            'no-var'                                            : 'error',
            'object-shorthand'                                  : 'error',
            'one-var'                                           : [
                'error',
                'never',
            ],
            'prefer-arrow/prefer-arrow-functions'               : 'error',
            'prefer-const'                                      : 'error',
            'prefer-template'                                   : 'error',
            quotes                                              : [
                'error',
                'single',
            ],
            radix                                               : 'error',
            'react/jsx-boolean-value'                           : 'off',
            'react/jsx-key'                                     : 'error',
            'react/jsx-no-bind'                                 : [
                'error',
                {
                    allowArrowFunctions : true,
                },
            ],
            'react/jsx-tag-spacing'                             : [
                'error',
                {
                    afterOpening : 'allow',
                    closingSlash : 'allow',
                },
            ],
            'react/react-in-jsx-scope'                          : 'off',
            'react/self-closing-comp'                           : 'error',
            semi                                                : 'error',
            'spaced-comment'                                    : [
                'error',
                'always',
                {
                    markers : [
                        '/'
                    ],
                },
            ],
            'stylistic/indent'                                  : [
                'error',
                4,
                {
                    ArrayExpression  : 'first',
                    ObjectExpression : 'first',
                    SwitchCase       : 1,
                },
            ],
            'stylistic/member-delimiter-style'                  : [
                'error',
                {
                    multiline  : {
                        delimiter   : 'comma',
                        requireLast : true,
                    },
                    singleline : {
                        delimiter   : 'comma',
                        requireLast : true,
                    },
                },
            ],
            'unicorn/prefer-switch'                             : [
                'error',
                {
                    minimumCases : 3,
                },
            ],
            'use-isnan'                                         : 'error',
            'valid-typeof'                                      : 'off',
        },
    },
]);

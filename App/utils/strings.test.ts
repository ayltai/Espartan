import { camelCaseToSnakeCase, snakeCaseToCamelCase, } from './strings';

describe('camelCaseToSnakeCase', () => {
    it('converts camelCase to snake_case', () => {
        const input = {
            camelCaseKey : 'value',
            nestedObject : {
                anotherCamelCaseKey : 'anotherValue',
            },
        };

        const expectedOutput = {
            camel_case_key : 'value',
            nested_object  : {
                another_camel_case_key : 'anotherValue',
            },
        };

        expect(camelCaseToSnakeCase(input)).toEqual(expectedOutput);
    });

    it('returns non-object values as is', () => {
        expect(camelCaseToSnakeCase('string')).toBe('string');
    });
});

describe('snakeCaseToCamelCase', () => {
    it('converts snake_case to camelCase', () => {
        const input = {
            snake_case_key : 'value',
            nested_object  : {
                another_snake_case_key : 'anotherValue',
            },
        };

        const expectedOutput = {
            snakeCaseKey : 'value',
            nestedObject : {
                anotherSnakeCaseKey : 'anotherValue',
            },
        };

        expect(snakeCaseToCamelCase(input)).toEqual(expectedOutput);
    });

    it('returns non-object values as is', () => {
        expect(snakeCaseToCamelCase('string')).toBe('string');
    });
});

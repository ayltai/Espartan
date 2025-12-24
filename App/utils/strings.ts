export const camelCaseToSnakeCase = (obj : string | Record<string, any>) => {
    if (obj === null || typeof obj !== 'object') return obj;

    const result : Record<string, any> = {};

    Object.keys(obj).forEach(key => {
        const newKey = key.replace(/(([a-z])(?=[A-Z][a-zA-Z])|([A-Z])(?=[A-Z][a-z]))/g,'$1_').toLowerCase();
        result[newKey] = camelCaseToSnakeCase(obj[key]);
    });

    return result;
};

export const snakeCaseToCamelCase = (obj : string | Record<string, any>) => {
    if (obj === null || typeof obj !== 'object') return obj;

    const result : Record<string, any> = {};

    Object.keys(obj).forEach(key => {
        const newKey = key.replace(/_([a-z])/g, group => group[1].toUpperCase());
        result[newKey] = snakeCaseToCamelCase(obj[key]);
    });

    return result;
};

export const capitaliseFirstLetter = (str : string) : string => {
    if (typeof str !== 'string' || str.length === 0) return str;

    return str.charAt(0).toUpperCase() + str.slice(1);
};

export const formatMacAddress = (mac : string | undefined) : string | undefined => mac ? mac.toUpperCase().match(/.{1,2}/g)?.join('-') : mac;

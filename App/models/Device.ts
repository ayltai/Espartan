export type Device = {
    id            : string,
    displayName?  : string,
    capabilities? : string,
    parameters?   : Record<string, string | number | boolean>,
    lastSeen      : string,
};

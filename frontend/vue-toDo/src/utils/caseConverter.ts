/**
 * Converts snake_case keys to camelCase in an object
 * @param obj Object with snake_case keys
 * @returns Object with camelCase keys
 */
export function snakeToCamel<T>(obj: any): T {
  if (obj === null || obj === undefined || typeof obj !== 'object') {
    return obj;
  }

  if (Array.isArray(obj)) {
    return obj.map(item => snakeToCamel<any>(item)) as unknown as T;
  }

  return Object.keys(obj).reduce((acc, key) => {
    // Convert snake_case to camelCase
    const camelKey = key.replace(/_([a-z])/g, (_, letter) => letter.toUpperCase());
    
    // Apply recursively to nested objects
    const value = obj[key];
    acc[camelKey] = value !== null && typeof value === 'object' 
      ? snakeToCamel(value) 
      : value;
    
    return acc;
  }, {} as any) as T;
}

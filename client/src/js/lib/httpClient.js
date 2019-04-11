export default class FetchHttpClient {

    constructor(baseUrl) {
        this.baseUrl = baseUrl || '';
        this.middlewareId = 1;
        this.middlewares = [];
    }

    addMiddleware(middleware) {
        if (!middleware.middlewareId) {
          middleware.middlewareId = this.middlewareId++;
        }
        this.middlewares.push(middleware);
    
        return this;
    }
    

    fetch(path, options = {}) {

        options = { headers: {}, ...options };
    
        const url = this.resolveUrl(path, options.uriParams || {});
        const responseMiddlewares = [];
        const requestPromise = this.middlewares.reduce(
            (promise, middleware) => promise.then(request => {
                const result = middleware(request);
                if (typeof result === 'function') {
                    responseMiddlewares.push(result);
                }
                return (result && typeof result !== 'function') ? result : request;
            }),
            Promise.resolve({ url, path, options, fetch })
        ).then(request => request.fetch(request.url, request.options));
    
        return requestPromise.then(response => responseMiddlewares.reduce(
            (promise, middleware) => promise.then(response => middleware(response) || response),
            Promise.resolve(response)
        ));
    }
    

    request(path, method, options = {}) {
        return this.fetch(path, { ...options, method });
    }

    get(path, options = {}) {
        return this.request(path, 'GET', options);
    }

    post(path, options = {}) {
        return this.request(path, 'POST', options);
    }

    put(path, options = {}) {
        return this.request(path, 'PUT', options);
    }

    delete(path, options = {}) {
        return this.request(path, 'DELETE', options);
    }

    resolveUrl(path, variables = {}) {
        if (path.toLowerCase().startsWith('http://')
            || path.toLowerCase().startsWith('https://')
            || path.startsWith('//')) {
            return path;
        }
    
        const baseUrl = this.baseUrl.replace(/\/+$/g, '');
        let fullUrl = '';
    
        if (path.startsWith('/')) {
            const rootPos = baseUrl.indexOf('/', baseUrl.indexOf('//') + 2);
            fullUrl = baseUrl.substr(0, rootPos === -1 ? undefined : rootPos) + path;
        } else {
            fullUrl = `${baseUrl}/${path}`;
        }
    
        fullUrl = fullUrl.replace(/\{(\w+)\}/ig, (match, group) => {
            if (!variables[group]) throw new Error(`Unknown path variable '${group}'.`);
            return encodeURIComponent(variables[group]);
        });
    
        return fullUrl;
    }

}


// JSON middleware
export const json = () => request => {
    if (request.options.json) {
        request.options.body = JSON.stringify(request.options.json);
        request.options.headers['Content-Type'] = 'application/json';
    }
    request.options.headers.Accept = 'application/json';
  
    return response => {
        const contentType = response.headers.get('Content-Type') || '';
        if (contentType.indexOf('json') === -1) return response;
        return response.json().then(json => (response.jsonData = json, response));
    };
};
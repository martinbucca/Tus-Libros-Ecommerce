export class ApiResponse {

    static understandThis(aRawResponse) {
        throw new Error("You have to implement the method");
    }

    static defaultResponse() {
        throw new Error("You have to implement the method");
    }

    constructor(aRawResponse) {
        this._rawResponse = aRawResponse;
    }

    static asDefaultResponse() {
        const content = this.defaultResponse();
        return new this(content);
    }

    hasError() {
        return this.errors().length >= 1
    }

    errors() {
        throw new Error("You have to implement the method");
    }

}
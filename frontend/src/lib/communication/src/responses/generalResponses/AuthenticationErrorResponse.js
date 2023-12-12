import {ApiErrorResponse} from "./ApiErrorResponse";

export class AuthenticationErrorResponse extends ApiErrorResponse {
    static defaultResponse() {
        return {
            "object": null,
            "errors": [
                {
                    "code": "authentication_error",
                    "text": ""
                }
            ]
        }
    }

    static errorCodes() {
        return ["authentication_error", 'token_expired'];
    }
}
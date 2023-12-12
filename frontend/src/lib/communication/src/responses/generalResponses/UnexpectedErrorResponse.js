import {ApiErrorResponse} from "./ApiErrorResponse";

export class UnexpectedErrorResponse extends ApiErrorResponse {
    static errorCodes() {
        return ["unexpected_error_code"];
    }
}
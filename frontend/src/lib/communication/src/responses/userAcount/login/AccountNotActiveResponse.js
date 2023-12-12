import {ApiErrorResponse} from "../../generalResponses/ApiErrorResponse";

export class AccountNotActiveResponse extends ApiErrorResponse {
    static defaultResponse() {
        return {
            "object": null,
            "errors": [
                {
                    "code": "account_not_active",
                    "text": "Tenés que confirmar la cuenta antes de hacer login"
                }
            ]
        }
    }

    static errorCodes() {
        return ["account_not_active"]
    }
}
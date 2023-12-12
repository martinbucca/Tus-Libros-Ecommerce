import {ApiErrorResponse} from "../../generalResponses/ApiErrorResponse";

export class UserMustRecoverPassword extends ApiErrorResponse {
    static defaultResponse() {
        return {
            "object": {
                "recover_password_token": "token"
            },
            "errors": [
                {
                    "code": "user_has_unusable_password_and_must_recover_it",
                    "text": "Tenés que recuperar tu contraseña para poder continuar"
                }
            ]
        }
    }

    static errorCodes() {
        return ["user_has_unusable_password_and_must_recover_it"]
    }

    recoverPasswordToken() {
        return this.content().recover_password_token
    }
}
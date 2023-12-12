import {ApiErrorResponse} from "../../generalResponses/ApiErrorResponse";


export class ParameterErrorResponse extends ApiErrorResponse {
    static defaultResponse() {
        return {
            "object": null,
            "errors": [
            {
                "code": "parameter_error",
                "text": "Password is too short (minimum is 6 characters)",
                "parameter_name": "password"
            },
                {
                    "code": "parameter_error",
                    "text": "Password does not meet the minimum system requirements. It should be composed of uppercase and lowercase letters, and numbers.",
                    "parameter_name": "password"
                },
                {
                    "code": "parameter_error",
                    "text": "Password has previously appeared in a data breach and should never be used. Please choose something harder to guess.",
                    "parameter_name": "password"
                }
        ]
        }
    }

    static errorCodes() {
        return ["parameter_error", "parameter_validation_error"];
    }

    customErrorMessages() {
        return {
            email: "Email inválido",
            password: "Contraseña inválida"
        }
    }

    fieldErrors() {
        let parameterErrors = {};
        this.errors().forEach(error => {
            const parameterName = error['parameter_name'];
            let errorMessage = this.customErrorMessages()[parameterName];
            if (parameterName === "password" && error["text"].includes("breach")) {
                errorMessage = "Esta contraseña fue filtrada o es muy simple. Elija otra"
            }
            parameterErrors[parameterName] = errorMessage;
        });

        return parameterErrors;
    }

    generalErrors(){
        return {}
    }
}

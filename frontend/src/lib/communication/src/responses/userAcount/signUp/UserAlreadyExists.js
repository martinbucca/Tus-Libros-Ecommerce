import {ApiErrorResponse} from "../../generalResponses/ApiErrorResponse";


export class UserAlreadyExists extends ApiErrorResponse {
    static defaultResponse() {
        // TODO: Definir respuesta por defecto
    }

    static errorCodes() {
        return ["user_already_exists"];
    }

    fieldErrors() {
        return {}
    }

    generalErrors(){
        return {general: 'El usuario no es válido o ya existe.'}
    }

}


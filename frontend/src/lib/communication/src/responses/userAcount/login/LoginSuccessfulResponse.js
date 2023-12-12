import {SuccessfulApiResponse} from "../../generalResponses/SuccessfulApiResponse";

export class LoginSuccessfulResponse extends SuccessfulApiResponse {
    static defaultResponse() {
        return {
            "object": {
                "token": "26d17591bfa86a3b3d197436d400dce22a70728f",
                "user_id": 123,
                "email": "juansito@gmail.com",
                "first_name": "JUAN",
                "last_name": "PEREZ CASTRO",
                "real_state_name": "InmoTest",
            },
            "errors": []
        }
    }
}
import {SuccessfulApiResponse} from "../../generalResponses/SuccessfulApiResponse";

export class SignUpSuccessfulResponse extends SuccessfulApiResponse {
    static defaultResponse() {
        return {
            "object": {
                "id": 2,
                "email": "email@test.com"
            },
            "errors": []
        }
    }
}
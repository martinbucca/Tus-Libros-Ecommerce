import {ApiResponse} from "../response"

export class SuccessfulApiResponse extends ApiResponse {

    static understandThis(jsonResponse) {
        return jsonResponse.errors && jsonResponse.errors.length === 0;
    }
}
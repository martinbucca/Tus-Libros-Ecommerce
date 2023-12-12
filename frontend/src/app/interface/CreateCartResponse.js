import {ApiResponse} from "../../lib/communication/src/responses/response";


export class CreateCartResponse extends ApiResponse {

    static understandThis(aRawResponse) {
        const result = aRawResponse.split('|');
        const code = result[0];
        return code == '0';
    }

    static defaultResponse() {
        return '0|123456789';
    }


    errors() {
        return []
    }

    cartId(){
        return this._rawResponse.split('|')[1];
    }
}
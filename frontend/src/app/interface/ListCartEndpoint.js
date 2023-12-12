import {Endpoint} from "../../lib/communication/src/endpoints/endpoint";
import {CartResponse} from "./CartResponse";
import {ErrorResponse} from "./ErrorResponse";


export class ListCartEndpoint extends Endpoint {

    url() {
        return 'listCart'
    }

    method() {
        return this.constructor.getMethod()
    }

    ownResponses() {
        return [CartResponse, ErrorResponse]
    }

    needsAuthorization() {
        return false;
    }
}
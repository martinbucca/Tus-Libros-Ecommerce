import {Endpoint} from "../../lib/communication/src/endpoints/endpoint";
import {CreateCartResponse} from "./CreateCartResponse";
import {ErrorResponse} from "./ErrorResponse";


export class CreateCartEndpoint extends Endpoint {

    url() {
        return 'createCart'
    }

    method() {
        return this.constructor.getMethod()
    }

    ownResponses() {
        return [CreateCartResponse, ErrorResponse]
    }

    needsAuthorization() {
        return false;
    }
}
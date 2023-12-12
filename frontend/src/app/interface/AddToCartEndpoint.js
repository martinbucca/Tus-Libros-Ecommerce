import {Endpoint} from "../../lib/communication/src/endpoints/endpoint";
import {ErrorResponse} from "./ErrorResponse";
import {ItemAddedToCartResponse} from "./ItemAddedToCartResponse";


export class AddToCartEndpoint extends Endpoint {

    url() {
        return 'addToCart'
    }

    method() {
        return this.constructor.getMethod()
    }

    ownResponses() {
        return [ItemAddedToCartResponse, ErrorResponse]
    }

    needsAuthorization() {
        return false;
    }
}
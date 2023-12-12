import {Endpoint} from "../../lib/communication/src/endpoints/endpoint";
import {ErrorResponse} from "./ErrorResponse";
import {SuccessfulCheckoutResponse} from "./SuccessfulCheckoutResponse";


export class CheckoutCartEndpoint extends Endpoint {

    url() {
        return 'checkOutCart'
    }

    method() {
        return this.constructor.getMethod()
    }

    ownResponses() {
        return [SuccessfulCheckoutResponse, ErrorResponse]
    }

    needsAuthorization() {
        return false;
    }
}
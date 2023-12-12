import {Endpoint} from "../../lib/communication/src/endpoints/endpoint";
import {ErrorResponse} from "./ErrorResponse";
import {ListPurchasesResponse} from "./ListPurchasesResponse";


export class ListPurchasesEndpoint extends Endpoint {

    url() {
        return 'listPurchases'
    }

    method() {
        return this.constructor.getMethod()
    }

    ownResponses() {
        return [ListPurchasesResponse, ErrorResponse]
    }

    needsAuthorization() {
        return false;
    }
}
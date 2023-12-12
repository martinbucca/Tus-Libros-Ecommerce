import {ApiClient} from "../../lib/communication/src";
import {ListCartEndpoint} from "./ListCartEndpoint";
import {CreateCartEndpoint} from "./CreateCartEndpoint";
import {AddToCartEndpoint} from "./AddToCartEndpoint";
import {CheckoutCartEndpoint} from "./CheckoutCartEndpoint";
import {ListPurchasesEndpoint} from "./ListPurchasesEndpoint";


export class TusLibrosRestInterface extends ApiClient {

    createCart(aClientId, aPassword) {
        const values = {clientId: aClientId, password: aPassword};
        const endpoint = new CreateCartEndpoint();
        return this._callEndpoint(endpoint, values);
    }

    listCart(aCartId){
        const values = {cartId: aCartId};
        const endpoint = new ListCartEndpoint();
        return this._callEndpoint(endpoint, values);
    }

    addToCart(aBook, aQuantity, aCart){
        const values = {
            bookIsbn: aBook.isbn,
            bookQuantity: aQuantity.toString(),
            cartId: aCart.id
        };
        const endpoint = new AddToCartEndpoint();
        return this._callEndpoint(endpoint, values);
    }

    checkout(aCard, aCart) {
        const values = {
            cartId: aCart.id,
            ccn: aCard.number,
            cced: aCard.expiry,
            cco: aCard.name
        };
        const endpoint = new CheckoutCartEndpoint();
        return this._callEndpoint(endpoint, values);
    }

    listPurchases(aClientId, aPassword) {
        const values = {clientId: aClientId, password: aPassword};
        const endpoint = new ListPurchasesEndpoint();
        return this._callEndpoint(endpoint, values);
    }

}
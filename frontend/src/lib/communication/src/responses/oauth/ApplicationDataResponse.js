import { SuccessfulApiResponse } from "../generalResponses/SuccessfulApiResponse";


export class ApplicationDataResponse extends SuccessfulApiResponse {
    static defaultResponse() {
        return {
            object: {
                redirect_to: 'http://oauth.buenbit.local/callback?code=asd123',
            },
        }
    }

    clientId() {
        return this.content().client_id;
    }

    redirectUris() {
        return this.content().redirect_uris;
    }

    name() {
        return this.content().name;
    }

    logo() {
        return this.content().logo;
    }

    site() {
        return this.content().site;
    }
}
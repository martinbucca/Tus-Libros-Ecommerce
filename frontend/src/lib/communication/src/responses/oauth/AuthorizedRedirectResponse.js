import {SuccessfulApiResponse} from "../generalResponses/SuccessfulApiResponse";

export class AuthorizedRedirectResponse extends SuccessfulApiResponse {
    static defaultResponse() {
        return {
            object: {
                redirect_to: 'http://oauth.buenbit.local/callback?code=asd123',
            },
        }
    }

    redirectionTarget() {
        return this.content().redirect_to;
    }
}
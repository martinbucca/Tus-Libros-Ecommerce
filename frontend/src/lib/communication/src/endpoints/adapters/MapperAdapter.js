import {BaseMapperAdapter} from "./BaseMapperAdapter";

export class MapperAdapter extends BaseMapperAdapter {

    constructor(mapping) {
        super();
        this._mapping = mapping;
    }

    static newWithMapping(mapping) {
        return new this(mapping)
    }

    mapping() {
        return this._mapping
    }

}

package com.gm.gislain.tvshowapp.Model;

/**
 * Created by Gislain on 25/11/2016.
 */

public class Creator {

    private int id;
    private String creator;

    public static final String KEY_ID = "id";
    public static final String KEY_CREATOR = "creator";

    public Creator() {}

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getCreator() {
        return creator;
    }

    public void setCreator(String creator) {
        this.creator = creator;
    }
}

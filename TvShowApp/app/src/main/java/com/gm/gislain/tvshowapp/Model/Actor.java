package com.gm.gislain.tvshowapp.Model;

/**
 * Created by Gislain on 27/11/2016.
 */

public class Actor {

    private int id;
    private String name;

    public static final String KEY_ID = "id";
    public static final String KEY_NAME = "name";

    public Actor(){}

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }
}

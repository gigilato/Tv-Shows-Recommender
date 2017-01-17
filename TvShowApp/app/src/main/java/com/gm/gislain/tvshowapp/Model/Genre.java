package com.gm.gislain.tvshowapp.Model;

/**
 * Created by Gislain on 25/11/2016.
 */

public class Genre {

    private int id;
    private String genre;

    public static final String KEY_ID = "id";
    public static final String KEY_GENRE = "genre";

    public Genre() {}

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getGenre() {
        return genre;
    }

    public void setGenre(String genre) {
        this.genre = genre;
    }
}

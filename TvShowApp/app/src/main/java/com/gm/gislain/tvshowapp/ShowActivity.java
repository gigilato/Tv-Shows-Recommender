package com.gm.gislain.tvshowapp;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.RatingBar;
import android.widget.RelativeLayout;
import android.widget.TextView;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonArrayRequest;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;
import com.bumptech.glide.Glide;
import com.gm.gislain.tvshowapp.Model.Actor;
import com.gm.gislain.tvshowapp.Model.Creator;
import com.gm.gislain.tvshowapp.Model.Genre;
import com.gm.gislain.tvshowapp.Model.Network;
import com.gm.gislain.tvshowapp.Model.Show;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;

public class ShowActivity extends AppCompatActivity {

    private static String SHOW_URL = "http://10.0.2.2:5000/shows/id/";
    private static String SIMILARE_SHOW_URL = "http://10.0.2.2:5000/shows/similare/id/";
    private int MARGIN_END = 20;
    private int SIZE = 500;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_show);

        int showId = getIntent().getIntExtra("showId",0);

        getShowInfos(showId);
        getSimilareShows(showId);
    }

    public void getShowInfos(final int showId){
        String URL = SHOW_URL + showId;

        JsonObjectRequest objectRequest = new JsonObjectRequest(
                Request.Method.GET, URL, null, new Response.Listener<JSONObject>() {
            @Override
            public void onResponse(JSONObject response) {
                try {
                    Show show = new Show();

                    show.setName(response.getString(Show.KEY_NAME));
                    show.setPoster(response.getString(Show.KEY_POSTER));
                    show.setVotes(response.getDouble(Show.KEY_VOTES));
                    show.setSeasons(response.getInt(Show.KEY_SEASONS));
                    show.setDate(response.getString(Show.KEY_DATE));
                    show.setStatus(response.getString(Show.KEY_STATUS));
                    show.setOverview(response.getString(Show.KEY_OVERVIEW));
                    show.setBackdrop(response.getString(Show.KEY_BACKDROP));

                    System.out.println(show.getDate());
                    try {
                        JSONArray jsonArrayNetworks = response.getJSONArray(Show.KEY_NETWORKS);
                        ArrayList<Network> networks = new ArrayList<>();
                        for (int i = 0; i < jsonArrayNetworks.length(); i++) {
                            JSONObject object = jsonArrayNetworks.getJSONObject(i);
                            Network network = new Network();
                            network.setId(object.getInt(Network.KEY_ID));
                            network.setNetwork(object.getString(Network.KEY_NETWORK));
                            networks.add(network);
                        }

                        show.setNetworks(networks);
                    } catch (JSONException je) {}

                    try {
                        JSONArray jsonArrayGenres = response.getJSONArray(Show.KEY_GENRES);
                        ArrayList<Genre> genres = new ArrayList<>();
                        for (int i = 0; i < jsonArrayGenres.length(); i++) {
                            JSONObject object = jsonArrayGenres.getJSONObject(i);
                            Genre genre = new Genre();
                            genre.setId(object.getInt(Genre.KEY_ID));
                            genre.setGenre(object.getString(Genre.KEY_GENRE));
                            genres.add(genre);
                        }

                        show.setGenres(genres);
                    } catch (JSONException je) {}

                    try {
                        JSONArray jsonArrayActors = response.getJSONArray(Show.KEY_ACTORS);
                        ArrayList<Actor> actors = new ArrayList<>();
                        for (int i = 0; i < jsonArrayActors.length(); i++) {
                            JSONObject object = jsonArrayActors.getJSONObject(i);
                            Actor actor = new Actor();
                            actor.setId(object.getInt(Actor.KEY_ID));
                            actor.setName(object.getString(Actor.KEY_NAME));
                            actors.add(actor);
                        }
                        show.setActors(actors);
                    } catch (JSONException je) {}

                    try {
                        JSONArray jsonArrayCreators = response.getJSONArray(Show.KEY_CREATORS);
                        ArrayList<Creator> creators = new ArrayList<>();
                        for (int i = 0; i < jsonArrayCreators.length(); i++) {
                            JSONObject object = jsonArrayCreators.getJSONObject(i);
                            Creator creator = new Creator();
                            creator.setId(object.getInt(Creator.KEY_ID));
                            creator.setCreator(object.getString(Creator.KEY_CREATOR));
                            creators.add(creator);
                        }

                        show.setCreators(creators);
                    } catch (JSONException je) {}

                    setUpUI(show);

                } catch (JSONException e) {
                    e.printStackTrace();
                }
            }
        }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                Toast.makeText(getApplicationContext(), error.getMessage(), Toast.LENGTH_LONG).show();
            }
        });

        RequestQueue requestQueue = Volley.newRequestQueue(this);
        requestQueue.add(objectRequest);
    }

    public void setUpUI(Show show){
        RelativeLayout relativeLayout = (RelativeLayout) findViewById(R.id.layout_backdrop);
        ImageView imageView = (ImageView) findViewById(R.id.backdrop_imageview);
        TextView textViewTitle = (TextView) findViewById(R.id.show_title_textview);
        RatingBar ratingBar = (RatingBar) findViewById(R.id.rating);
        TextView textViewYear = (TextView) findViewById(R.id.year);
        TextView textViewNetwork = (TextView) findViewById(R.id.network);
        TextView textViewSeasons = (TextView) findViewById(R.id.seasons);
        TextView textViewStatus = (TextView) findViewById(R.id.status);
        TextView textViewActors = (TextView) findViewById(R.id.actors);
        TextView textViewOverview = (TextView) findViewById(R.id.overview);

        Glide.with(getApplicationContext())
                .load("http://" + show.getBackdrop())
                .into(imageView);

        relativeLayout.setMinimumHeight(imageView.getHeight());

        textViewTitle.setText(show.getName());
        ratingBar.setRating((float)show.getVotes() / 2);
        if(show.getDate() != null){
            String year = show.getDate().split(" ")[3];
            textViewYear.setText(year);
        }else textViewYear.setText("N/A");

        if(show.getNetworks() != null){
            String network = show.getNetworks().get(0).getNetwork();
            if(network.length() > 5){
                String[] tab = network.split(" ");
                String abrev = "";
                for(String s : tab) abrev += s.charAt(0);
                textViewNetwork.setText(abrev);
            }else textViewNetwork.setText(network);
        }
        else textViewNetwork.setText("N/A");

        if(show.getSeasons() != 0) textViewSeasons.append(show.getSeasons().toString());
        else textViewSeasons.setText("N/A");

        if(show.getStatus() != null){
            String status = show.getStatus();
            if(status.length() > 5) textViewStatus.setText("On air");
            else textViewStatus.setText(status);
        }
        else textViewStatus.setText("N/A");

        for(int i = 0 ; i < 2 && show.getActors() != null && i < show.getActors().size() ; i++) {
            textViewActors.append(show.getActors().get(i).getName());
            if(i != show.getActors().size() - 1 && i != 1) textViewActors.append(", ");
        }

        if(show.getOverview() != null) textViewOverview.setText(show.getOverview());
        else textViewOverview.setText("N/A");
    }


    private void getSimilareShows(int showId){
        String URL = SIMILARE_SHOW_URL + showId;
        JsonArrayRequest jsonArrayRequest = new JsonArrayRequest(
                URL, new Response.Listener<JSONArray>() {
            @Override
            public void onResponse(JSONArray response) {
                ArrayList<Show> shows = new ArrayList<>();

                for (int i = 0; i < response.length(); i++) {
                    try {
                        JSONObject object = response.getJSONObject(i);
                        Show show = new Show();
                        show.setId(object.getInt(Show.KEY_ID));
                        show.setPoster(object.getString(Show.KEY_POSTER));
                        shows.add(show);

                    } catch (JSONException e) {
                        e.printStackTrace();
                    }
                }

                LinearLayout layout = (LinearLayout) findViewById(R.id.similaire_shows);

                for (final Show show : shows){
                    ImageView imageView = new ImageView(getApplicationContext());
                    imageView.setClickable(true);
                    imageView.setScaleType(ImageView.ScaleType.FIT_CENTER);


                    LinearLayout.LayoutParams layoutParams = new LinearLayout.LayoutParams(
                            LinearLayout.LayoutParams.MATCH_PARENT, LinearLayout.LayoutParams.WRAP_CONTENT);

                    layoutParams.setMarginEnd(MARGIN_END);

                    imageView.setLayoutParams(layoutParams);

                    Glide.with(getApplicationContext())
                            .load("http://" + show.getPoster())
                            .override(SIZE,SIZE)
                            .into(imageView);

                    layout.addView(imageView);
                }
            }
        }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                error.printStackTrace();
                Toast.makeText(getApplicationContext(),"Error loading database",Toast.LENGTH_LONG).show();
            }
        });

        RequestQueue requestQueue = Volley.newRequestQueue(this);
        requestQueue.add(jsonArrayRequest);
    }
}

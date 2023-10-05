#include <gtk/gtk.h>

#define WIDTH 400
#define HEIGHT 400
#define M_PI 3.1415
// Data points to be plotted
double x[] = {1.0, 2.0, 3.0, 4.0, 5.0};
double y[] = {2.0, 3.0, 1.0, 4.0, 5.0};
int num_points = 5;


static void do_drawing(cairo_t *cr) {
    int i;

    // Set up a white background
    cairo_set_source_rgb(cr, 1, 1, 1);
    cairo_paint(cr);

    // Set up a blue color for the points
    cairo_set_source_rgb(cr, 0, 0, 1);
    cairo_set_line_width(cr, 2);

    // Plot the data points as circles
    for (i = 0; i < num_points; i++) {
        cairo_arc(cr, x[i] * WIDTH / 7, HEIGHT - y[i] * HEIGHT / 7, 5, 0, 2 * M_PI);
        cairo_fill(cr);
    }
}

static gboolean on_draw_event(GtkWidget *widget, cairo_t *cr, gpointer user_data) {
    do_drawing(cr);
    return FALSE;
}

int main(int argc, char *argv[]) {
    GtkWidget *window;
    GtkWidget *darea;

    gtk_init(&argc, &argv);

    window = gtk_window_new(GTK_WINDOW_TOPLEVEL);
    darea = gtk_drawing_area_new();
    gtk_container_add(GTK_CONTAINER(window), darea);

    g_signal_connect(G_OBJECT(darea), "draw", G_CALLBACK(on_draw_event), NULL);
    g_signal_connect(window, "destroy", G_CALLBACK(gtk_main_quit), NULL);

    gtk_window_set_position(GTK_WINDOW(window), GTK_WIN_POS_CENTER);
    gtk_window_set_default_size(GTK_WINDOW(window), WIDTH, HEIGHT);
    gtk_window_set_title(GTK_WINDOW(window), "Scatter Plot");

    gtk_widget_show_all(window);

    gtk_main();

    return 0;
}


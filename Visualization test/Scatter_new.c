#include <gtk/gtk.h>
#include <math.h>

#define WIDTH 800
#define HEIGHT 600
#define MARGIN 50
#define NUM_POINTS 100
#define AXIS_ARROW_SIZE 10

typedef struct {
    double x;
    double y;
    double intensity;
} DataPoint;

static void draw(GtkWidget *widget, cairo_t *cr, gpointer data) {
    DataPoint *points = (DataPoint *)data;
    GdkRGBA color;

    // Clear the background
    gdk_rgba_parse(&color, "white");
    gdk_cairo_set_source_rgba(cr, &color);
    cairo_paint(cr);

    // Draw X and Y axes with arrows
    gdk_rgba_parse(&color, "black");
    gdk_cairo_set_source_rgba(cr, &color);
    cairo_set_line_width(cr, 2.0);

    // X-axis
    cairo_move_to(cr, MARGIN, HEIGHT - MARGIN);
    cairo_line_to(cr, WIDTH - MARGIN, HEIGHT - MARGIN);
    cairo_move_to(cr, WIDTH - MARGIN - AXIS_ARROW_SIZE, HEIGHT - MARGIN - AXIS_ARROW_SIZE);
    cairo_line_to(cr, WIDTH - MARGIN, HEIGHT - MARGIN);
    cairo_move_to(cr, WIDTH - MARGIN - AXIS_ARROW_SIZE, HEIGHT - MARGIN + AXIS_ARROW_SIZE);
    cairo_line_to(cr, WIDTH - MARGIN, HEIGHT - MARGIN);

    // Y-axis
    cairo_move_to(cr, MARGIN, MARGIN);
    cairo_line_to(cr, MARGIN, HEIGHT - MARGIN);
    cairo_move_to(cr, MARGIN - AXIS_ARROW_SIZE, MARGIN + AXIS_ARROW_SIZE);
    cairo_line_to(cr, MARGIN, MARGIN);
    cairo_move_to(cr, MARGIN + AXIS_ARROW_SIZE, MARGIN + AXIS_ARROW_SIZE);
    cairo_line_to(cr, MARGIN, MARGIN);

    cairo_stroke(cr);

    // Draw data points
    for (int i = 0; i < NUM_POINTS; i++) {
        double x = points[i].x;
        double y = points[i].y;
        double intensity = points[i].intensity;

        // Map intensity to color (blue to red gradient)
        gdk_rgba_parse(&color, intensity < 0.5 ? "blue" : "red");

        // Scale and position the point
        x = MARGIN + (WIDTH - 2 * MARGIN) * x;
        y = HEIGHT - MARGIN - (HEIGHT - 2 * MARGIN) * y;

        gdk_cairo_set_source_rgba(cr, &color);
        cairo_arc(cr, x, y, 5.0, 0.0, 2 * G_PI);
        cairo_fill(cr);
    }
}

int main(int argc, char *argv[]) {
    gtk_init(&argc, &argv);

    // Create a GTK window
    GtkWidget *window = gtk_window_new(GTK_WINDOW_TOPLEVEL);
    gtk_window_set_title(GTK_WINDOW(window), "Scatter Plot");
    gtk_window_set_default_size(GTK_WINDOW(window), WIDTH, HEIGHT);
    g_signal_connect(window, "destroy", G_CALLBACK(gtk_main_quit), NULL);

    // Create a drawing area
    GtkWidget *draw_area = gtk_drawing_area_new();
    gtk_container_add(GTK_CONTAINER(window), draw_area);

    // Generate random data points with intensities
    DataPoint points[NUM_POINTS];
    for (int i = 0; i < NUM_POINTS; i++) {
        points[i].x = (double)rand() / RAND_MAX;
        points[i].y = (double)rand() / RAND_MAX;
        points[i].intensity = (double)rand() / RAND_MAX;
    }

    g_signal_connect(G_OBJECT(draw_area), "draw", G_CALLBACK(draw), points);

    gtk_widget_show_all(window);

    gtk_main();

    return 0;
}

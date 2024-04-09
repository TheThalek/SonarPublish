set(SRC
    sonarpublish.c
    sonarData.pb-c.c
    georeferencing.c
    networking.c
    )

set(HDR
    sonarData.pb-c.h
    georeferencing.h
    networking.h
    )

set(PUBLIC_HDR
    sonarpublish.h)

target_sources(${TARGET_LIB}
    PRIVATE ${SRC} ${HDR}
    PUBLIC ${PUBLIC_HDR}
)

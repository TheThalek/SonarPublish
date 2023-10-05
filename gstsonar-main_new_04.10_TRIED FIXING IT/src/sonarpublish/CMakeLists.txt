set(SRC
    sonarpublish.c
    )

set(HDR
    )

set(PUBLIC_HDR
    sonarpublish.h)

target_sources(${TARGET_LIB}
    PRIVATE ${SRC} ${HDR}
    PUBLIC ${PUBLIC_HDR}
)